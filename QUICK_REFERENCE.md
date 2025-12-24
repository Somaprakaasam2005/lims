# LIMS Quick Reference Guide

## Quick Start

```bash
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Initialize database
python bootstrap_db.py

# 3. Run application
python app.py

# 4. Open browser
http://localhost:5000

# 5. Login
Username: admin
Password: admin
```

---

## Test Data Format Reference

### Compressive Strength
**Format**: `load_kN,area_mm2`  
**Example**: `250,19600`  
**Route**: `/calculate/compressive/<test_id>`

### Flexural Strength
**Format**: `load_kN,length_mm,width_mm,depth_mm`  
**Example**: `45,500,150,150`  
**Route**: `/calculate/flexural/<test_id>`

### Split Tensile Strength ⭐ NEW
**Format**: `load_kN,length_mm,diameter_mm`  
**Example**: `120,300,150`  
**Route**: `/calculate/split_tensile/<test_id>`

### Water Absorption ⭐ NEW
**Format**: `dry_mass_g,saturated_mass_g`  
**Example**: `2000,2100`  
**Route**: `/calculate/water_absorption/<test_id>`

### Atterberg Limits
**Format**: `LL,PL`  
**Example**: `45,20`  
**Route**: `/calculate/atterberg/<test_id>`

### CBR Test ⭐ NEW
**Format**: `load_kN,standard_load_kN`  
**Example**: `10.5,13.24`  
**Route**: `/calculate/cbr/<test_id>`

### Proctor Compaction ⭐ NEW
**Format**: `dry_density_kgm3,water_content_%`  
**Example**: `1850,12.5`  
**Route**: `/calculate/proctor/<test_id>`

### Sieve Analysis
**Format**: `size1:mass1;size2:mass2;total:totalmass`  
**Example**: `75:10;37.5:20;19:30;total:95`  
**Route**: `/calculate/sieve/<test_id>`

---

## URL Routes Quick Reference

### Authentication
- `GET /login` - Login page
- `POST /login` - Login submission
- `GET /logout` - Logout

### Dashboard
- `GET /` or `/dashboard` - Main dashboard

### Projects
- `GET /projects` - List all projects
- `GET /projects/new` - New project form
- `POST /projects/new` - Create project
- `GET /projects/<id>/edit` - Edit project form
- `POST /projects/<id>/edit` - Update project
- `POST /projects/<id>/delete` - Delete project

### Samples
- `GET /samples` - List all samples
- `GET /samples/new` - New sample form
- `POST /samples/new` - Create sample
- `GET /samples/<id>` - Sample details
- `GET /samples/<id>/edit` - Edit sample
- `POST /samples/<id>/edit` - Update sample
- `POST /samples/<id>/delete` - Delete sample

### Tests
- `POST /samples/<id>/add_test` - Add test to sample
- `GET /calculate/<type>/<test_id>` - Calculate result
- `POST /test/<id>/approve` - Approve test
- `POST /test/<id>/reject` - Reject test

### Reports ⭐ ENHANCED
- `GET /reports/generate/<test_id>` - Single report
- `POST /reports/batch` - Batch report (multiple tests)

### Export ⭐ NEW
- `GET /export/samples` - Export samples to Excel
- `GET /export/tests` - Export tests to Excel

### Audit Logs ⭐ NEW
- `GET /audit_logs` - View audit trail (Admin only)

### Users (Admin only)
- `GET /users` - List users
- `GET /users/new` - New user form
- `POST /users/new` - Create user
- `GET /users/<id>/edit` - Edit user
- `POST /users/<id>/edit` - Update user
- `POST /users/<id>/delete` - Delete user

---

## Role Permissions Matrix

| Feature | Admin | Engineer | Lab Tech |
|---------|-------|----------|----------|
| Login/Logout | ✅ | ✅ | ✅ |
| View Dashboard | ✅ | ✅ | ✅ |
| Create Project | ✅ | ✅ | ❌ |
| Edit Project | ✅ | ✅ | ❌ |
| Delete Project | ✅ | ✅ | ❌ |
| Register Sample | ✅ | ✅ | ✅ |
| Add Test Data | ✅ | ✅ | ✅ |
| Approve Tests | ✅ | ✅ | ❌ |
| Generate Reports | ✅ | ✅ | ✅ |
| Export Excel | ✅ | ✅ | ❌ |
| View Audit Logs | ✅ | ❌ | ❌ |
| User Management | ✅ | ❌ | ❌ |

---

## Database Models

### User
- id, username, password_hash, role, created_at

### Project
- id, project_name, client_name, location, start_date, status, created_by

### Sample
- id, sample_id, project_id, sample_type, location, received_date

### TestResult
- id, sample_id, test_name, raw_values, calculated_result, status
- approved_by, approved_at, remarks, created_at

### Report
- id, sample_id, test_result_id, file_path, generated_by, created_at

### AuditLog ⭐ NEW
- id, user_id, action, entity_type, entity_id, details, timestamp

---

## Calculation Formulas

### Compressive Strength
```
σ = P / A
where P = Load (kN), A = Area (mm²)
Result in MPa
```

### Flexural Strength
```
σ = (P × L) / (b × d²)
where P = Load, L = span, b = width, d = depth
Result in MPa
```

### Split Tensile Strength ⭐
```
T = (2 × P) / (π × L × D)
where P = Load, L = length, D = diameter
Result in MPa
```

### Water Absorption ⭐
```
WA = ((Ws - Wd) / Wd) × 100
where Ws = saturated mass, Wd = dry mass
Result in %
```

### CBR ⭐
```
CBR = (Test Load / Standard Load) × 100
Result in %
```

### Proctor Compaction ⭐
```
Returns dry density and water content
For plotting compaction curve
```

### Atterberg Limits
```
PI = LL - PL
where LL = Liquid Limit, PL = Plastic Limit
```

### Sieve Analysis
```
Fineness Modulus = Σ(Cumulative % Retained) / 100
D10, D30, D60 calculated from grading curve
```

---

## Status Values

### Test Status
- `Pending` - Awaiting approval (yellow)
- `Approved` - Approved by Engineer/Admin (green)
- `Rejected` - Rejected (red)

### Project Status
- `Active` - Ongoing project (blue)
- `Completed` - Finished project (green)
- `On Hold` - Paused project (gray)

---

## File Locations

### Reports
- Path: `reports/report_<test_id>.pdf`
- Batch: `reports/batch_<sample_id>_<timestamp>.pdf`

### Excel Exports
- Samples: `samples_export_<timestamp>.xlsx`
- Tests: `tests_export_<timestamp>.xlsx`

### Database
- Dev: `instance/lims_dev.db` (SQLite)
- Prod: Configure MySQL in `.env`

---

## Environment Variables

Create `.env` file:
```
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///lims_dev.db
FLASK_DEBUG=False
```

For MySQL:
```
DATABASE_URI=mysql+pymysql://user:pass@localhost/lims_db
```

---

## Common Tasks

### Add New User
```
1. Login as Admin
2. Navigate to Users
3. Click "Create New User"
4. Enter username, password, select role
5. Submit
```

### Process New Sample
```
1. Create/Select Project
2. Register Sample (link to project)
3. Add Test (select type, enter raw data)
4. System calculates result automatically
5. Engineer approves/rejects
6. Generate PDF report
```

### Generate Batch Report
```
1. Go to Sample Details page
2. Check boxes next to tests
3. Click "Generate Batch Report for Selected"
4. PDF downloads automatically
```

### Export Data
```
1. Click "Export" in navigation
2. Select "Samples" or "Tests"
3. Excel file downloads automatically
```

### View Audit Trail (Admin)
```
1. Click "Audit Logs" in navigation
2. Filter by user/action/entity
3. Review compliance trail
```

---

## Troubleshooting

### Issue: Import errors
**Solution**: `python -m pip install -r requirements.txt`

### Issue: Database not found
**Solution**: `python bootstrap_db.py`

### Issue: Login fails
**Solution**: Use default credentials (admin/admin) or reset database

### Issue: CSRF token error
**Solution**: Ensure Flask-WTF installed: `pip install flask-wtf`

### Issue: Reports not generating
**Solution**: Check `reports/` directory exists and is writable

### Issue: Excel export fails
**Solution**: Ensure openpyxl installed: `pip install openpyxl`

---

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_calculations.py
pytest tests/test_integration.py
```

### Validation Script
```bash
python validate_enhancements.py
```

---

## Mobile Access

The system is mobile-responsive:
- Tablets: Optimized layout (769px - 1024px)
- Mobile: Full functionality (<768px)
- Small phones: Adjusted UI (<480px)

Navigate same URLs on mobile browser.

---

## Security Best Practices

1. **Change default admin password immediately**
2. **Use strong SECRET_KEY in production**
3. **Enable HTTPS in production**
4. **Regular database backups**
5. **Review audit logs monthly**
6. **Update dependencies regularly**
7. **Limit Admin role assignments**

---

## Support

- Documentation: [README.md](README.md)
- Setup Guide: [README_SETUP.md](README_SETUP.md)
- Enhancements: [ENHANCEMENTS.md](ENHANCEMENTS.md)
- Full Summary: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## Version Info

**Version**: 2.0 (Enhanced)  
**Status**: Production Ready  
**Last Updated**: 2024  
**Validation**: ✅ All tests passing
