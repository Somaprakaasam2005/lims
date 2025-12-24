"""
models.py - SQLAlchemy models for Civil Engineering LIMS

This file defines simple models: User, Sample, TestResult, Report.
It's intentionally simple and includes helper methods for password hashing.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# We'll create models at runtime when SQLAlchemy 'db' is available.
def init_models(db):
    """Create SQLAlchemy models dynamically once `db` is available.

    This avoids referencing db.Model at import time which breaks when the
    application injects the db instance after importing this module.
    """
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(30), nullable=False, default='Lab Technician')

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

    class Project(db.Model):
        __tablename__ = 'projects'
        id = db.Column(db.Integer, primary_key=True)
        project_code = db.Column(db.String(50), unique=True, nullable=False)
        project_name = db.Column(db.String(120), nullable=False)
        client_name = db.Column(db.String(120))
        description = db.Column(db.Text)
        created_at = db.Column(db.DateTime)
        status = db.Column(db.String(30), default='Active')  # Active, Completed, On Hold
        
        samples = db.relationship('Sample', backref='project', lazy=True)

    class Sample(db.Model):
        __tablename__ = 'samples'
        id = db.Column(db.Integer, primary_key=True)
        sample_id = db.Column(db.String(50), unique=True, nullable=False)
        sample_type = db.Column(db.String(50), nullable=False)  # Concrete, Soil, Aggregate
        project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
        project_name = db.Column(db.String(120))  # Kept for backward compatibility
        client_name = db.Column(db.String(120))
        date_collected = db.Column(db.String(30))

        tests = db.relationship('TestResult', backref='sample', lazy=True)

    class TestResult(db.Model):
        __tablename__ = 'test_results'
        id = db.Column(db.Integer, primary_key=True)
        sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'), nullable=False)
        test_name = db.Column(db.String(120), nullable=False)
        raw_values = db.Column(db.Text)  # Simple storage for raw values; could be JSON
        calculated_result = db.Column(db.Text)
        date_tested = db.Column(db.DateTime)
        status = db.Column(db.String(30), default='Pending')  # Pending, Approved, Rejected
        approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
        approved_at = db.Column(db.DateTime)
        remarks = db.Column(db.Text)
        
        approver = db.relationship('User', foreign_keys=[approved_by])

    class Report(db.Model):
        __tablename__ = 'reports'
        id = db.Column(db.Integer, primary_key=True)
        sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
        test_result_id = db.Column(db.Integer, db.ForeignKey('test_results.id'))
        file_path = db.Column(db.String(255))
        created_at = db.Column(db.DateTime)

    class AuditLog(db.Model):
        __tablename__ = 'audit_logs'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        action = db.Column(db.String(50), nullable=False)  # CREATE, UPDATE, DELETE, APPROVE, REJECT
        entity_type = db.Column(db.String(50), nullable=False)  # Sample, TestResult, Project, User
        entity_id = db.Column(db.Integer)
        details = db.Column(db.Text)  # JSON or text description
        timestamp = db.Column(db.DateTime, nullable=False)
        
        user = db.relationship('User', foreign_keys=[user_id])

    # Expose classes at module level so other modules can import them from models
    globals()['User'] = User
    globals()['Project'] = Project
    globals()['Sample'] = Sample
    globals()['TestResult'] = TestResult
    globals()['Report'] = Report
    globals()['AuditLog'] = AuditLog
