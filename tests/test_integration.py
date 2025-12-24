"""
Integration tests for Flask routes and workflows
"""
import pytest
import sys
import os

# Set test environment before importing app
os.environ['DATABASE_URI'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-secret'
os.environ['TESTING'] = 'True'

import app as myapp
from models import User, Sample, TestResult


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    myapp.app.config['TESTING'] = True
    myapp.app.config['WTF_CSRF_ENABLED'] = False
    
    with myapp.app.app_context():
        myapp.db.create_all()
        # Create test admin user
        admin = User(username='testadmin', role='Admin')
        admin.set_password('testpass')
        myapp.db.session.add(admin)
        myapp.db.session.commit()
    
    yield myapp.app
    
    with myapp.app.app_context():
        myapp.db.session.remove()
        myapp.db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """Create an authenticated test client."""
    client.post('/login', data={'username': 'testadmin', 'password': 'testpass'})
    return client


def test_login_required(client):
    """Test that login is required for protected routes."""
    response = client.get('/')
    assert response.status_code == 302  # Redirect to login


def test_login_success(client):
    """Test successful login."""
    response = client.post('/login', data={
        'username': 'testadmin',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'dashboard' in response.data


def test_login_failure(client):
    """Test failed login with wrong credentials."""
    response = client.post('/login', data={
        'username': 'testadmin',
        'password': 'wrongpass'
    })
    assert b'Invalid' in response.data or response.status_code == 200


def test_create_sample(auth_client):
    """Test creating a new sample."""
    response = auth_client.post('/samples/new', data={
        'sample_id': 'TEST-001',
        'sample_type': 'Concrete',
        'project_name': 'Test Project',
        'client_name': 'Test Client',
        'date_collected': '2025-01-01'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'TEST-001' in response.data


def test_view_samples(auth_client):
    """Test viewing samples list."""
    # Create a sample first
    auth_client.post('/samples/new', data={
        'sample_id': 'TEST-002',
        'sample_type': 'Soil',
        'project_name': 'Test',
        'client_name': 'Client'
    })
    
    response = auth_client.get('/samples')
    assert response.status_code == 200
    assert b'TEST-002' in response.data


def test_sample_detail(auth_client, app):
    """Test viewing sample details."""
    with app.app_context():
        # Create a sample
        sample = Sample(
            sample_id='TEST-003',
            sample_type='Aggregate',
            project_name='Test',
            client_name='Client'
        )
        myapp.db.session.add(sample)
        myapp.db.session.commit()
        sample_id = sample.id
    
    response = auth_client.get(f'/samples/{sample_id}')
    assert response.status_code == 200
    assert b'TEST-003' in response.data


def test_add_test_to_sample(auth_client, app):
    """Test adding a test result to a sample."""
    with app.app_context():
        sample = Sample(
            sample_id='TEST-004',
            sample_type='Concrete',
            project_name='Test',
            client_name='Client'
        )
        myapp.db.session.add(sample)
        myapp.db.session.commit()
        sample_id = sample.id
    
    response = auth_client.post(f'/samples/{sample_id}', data={
        'test_name': 'Compressive Strength',
        'raw_value': '250,19600'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_compressive_strength_calculation(auth_client, app):
    """Test compressive strength calculation."""
    with app.app_context():
        sample = Sample(sample_id='TEST-005', sample_type='Concrete', project_name='T', client_name='C')
        myapp.db.session.add(sample)
        myapp.db.session.commit()
        
        test = TestResult(sample_id=sample.id, test_name='Compressive Strength', raw_values='250,19600')
        myapp.db.session.add(test)
        myapp.db.session.commit()
        test_id = test.id
    
    response = auth_client.get(f'/calculate/compressive/{test_id}', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        test = TestResult.query.get(test_id)
        assert test.calculated_result is not None
        assert 'MPa' in test.calculated_result


def test_atterberg_calculation(auth_client, app):
    """Test Atterberg limits calculation."""
    with app.app_context():
        sample = Sample(sample_id='TEST-006', sample_type='Soil', project_name='T', client_name='C')
        myapp.db.session.add(sample)
        myapp.db.session.commit()
        
        test = TestResult(sample_id=sample.id, test_name='Atterberg Limits', raw_values='45,20')
        myapp.db.session.add(test)
        myapp.db.session.commit()
        test_id = test.id
    
    response = auth_client.get(f'/calculate/atterberg/{test_id}', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        test = TestResult.query.get(test_id)
        assert test.calculated_result is not None
        assert 'PI=' in test.calculated_result


def test_edit_sample(auth_client, app):
    """Test editing a sample."""
    with app.app_context():
        sample = Sample(sample_id='TEST-007', sample_type='Concrete', project_name='Old', client_name='C')
        myapp.db.session.add(sample)
        myapp.db.session.commit()
        sample_id = sample.id
    
    response = auth_client.post(f'/samples/{sample_id}/edit', data={
        'sample_id': 'TEST-007-EDITED',
        'sample_type': 'Soil',
        'project_name': 'New Project',
        'client_name': 'New Client',
        'date_collected': '2025-12-23'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        sample = Sample.query.get(sample_id)
        assert sample.sample_id == 'TEST-007-EDITED'
        assert sample.project_name == 'New Project'


def test_delete_sample(auth_client, app):
    """Test deleting a sample."""
    with app.app_context():
        sample = Sample(sample_id='TEST-008', sample_type='Concrete', project_name='T', client_name='C')
        myapp.db.session.add(sample)
        myapp.db.session.commit()
        sample_id = sample.id
    
    response = auth_client.post(f'/samples/{sample_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        sample = Sample.query.get(sample_id)
        assert sample is None


def test_logout(auth_client):
    """Test logout functionality."""
    response = auth_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify we're logged out by trying to access protected route
    response = auth_client.get('/')
    assert response.status_code == 302  # Redirect to login
