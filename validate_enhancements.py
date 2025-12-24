"""
Validation script for LIMS enhancements
Tests that all new functionality is properly integrated
"""

import sys
import os

def test_imports():
    """Test all required modules can be imported"""
    print("Testing imports...")
    try:
        import flask
        import flask_login
        import flask_sqlalchemy
        import openpyxl
        import reportlab
        from flask_wtf.csrf import CSRFProtect
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_calculations():
    """Test new calculation functions"""
    print("\nTesting calculation functions...")
    try:
        from calculations import (
            compressive_strength_mpa,
            flexural_strength_mpa,
            split_tensile_strength_mpa,
            water_absorption_percent,
            cbr_value,
            proctor_compaction,
            sieve_analysis_summary,
            atterberg_limits
        )
        
        # Test split tensile
        result = split_tensile_strength_mpa(120.0, 300.0, 150.0)
        assert result > 0, "Split tensile calculation failed"
        print(f"  Split Tensile (120kN, 300mm, 150mm): {result:.2f} MPa")
        
        # Test water absorption
        result = water_absorption_percent(2000.0, 2100.0)
        assert result == 5.0, "Water absorption calculation failed"
        print(f"  Water Absorption (2000g, 2100g): {result:.2f}%")
        
        # Test CBR
        result = cbr_value(10.5, 13.24)
        assert 79.0 < result < 80.0, "CBR calculation failed"
        print(f"  CBR (10.5kN, 13.24kN): {result:.2f}%")
        
        # Test Proctor (takes single dry_density and water_content)
        result = proctor_compaction(1850.0, 12.5)
        print(f"  Proctor: Dry Density = {result['dry_density']} kg/m³, Water Content = {result['water_content']}%")
        
        print("✅ All calculation functions working")
        return True
    except Exception as e:
        print(f"❌ Calculation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_models():
    """Test new model definitions"""
    print("\nTesting models...")
    try:
        # Import app to initialize models
        import app
        import models
        
        # Check AuditLog model exists in app.models (not models.py directly)
        assert hasattr(app.models, 'AuditLog'), "AuditLog model not found in app.models"
        
        # Check model has required fields
        audit_fields = ['user_id', 'action', 'entity_type', 'entity_id', 'details', 'timestamp']
        for field in audit_fields:
            assert hasattr(app.models.AuditLog, field), f"AuditLog missing field: {field}"
        
        print("✅ Models validated")
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates():
    """Test new template files exist"""
    print("\nTesting templates...")
    try:
        templates = [
            'templates/404.html',
            'templates/500.html',
            'templates/audit_logs.html'
        ]
        
        for template in templates:
            assert os.path.exists(template), f"Template not found: {template}"
            print(f"  ✓ {template}")
        
        print("✅ All templates exist")
        return True
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

def test_css():
    """Test responsive CSS added"""
    print("\nTesting CSS enhancements...")
    try:
        with open('static/style.css', 'r') as f:
            css = f.read()
        
        assert '@media' in css, "Responsive media queries not found"
        assert 'max-width: 768px' in css or 'max-width:768px' in css, "Mobile breakpoint not found"
        
        print("✅ Responsive CSS present")
        return True
    except Exception as e:
        print(f"❌ CSS test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("LIMS Enhancement Validation")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Calculations", test_calculations()))
    results.append(("Models", test_models()))
    results.append(("Templates", test_templates()))
    results.append(("CSS", test_css()))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:15} : {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All validation tests PASSED!")
        print("The LIMS system is ready for deployment.")
    else:
        print("⚠️  Some tests FAILED. Please review errors above.")
        sys.exit(1)
    print("=" * 60)

if __name__ == '__main__':
    main()
