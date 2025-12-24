# Running the LIMS Application

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Quick Start

### 1. Install Dependencies
```powershell
# If you haven't already created a virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Database
Create a `.env` file in the project root:
```
DATABASE_URI=sqlite:///lims_dev.db
SECRET_KEY=your-secret-key-change-in-production
```

For MySQL (if preferred):
```
DATABASE_URI=mysql+pymysql://user:password@localhost/lims_db
SECRET_KEY=your-secret-key
```

### 3. Initialize Database
```powershell
# Run the bootstrap script to create tables and add sample data
python bootstrap_db.py
```

### 4. Run the Application
```powershell
# Option 1: Direct run
python app.py

# Option 2: Using the PowerShell script
.\run_dev.ps1
```

The application will be available at: **http://localhost:5000**

## Default Login Credentials

After running `bootstrap_db.py`, use these credentials:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| tech | tech123 | Lab Technician |
| engineer | eng123 | Engineer |

## Application Structure

```
/lims
├── app.py              # Main Flask application
├── models.py           # Database models
├── calculations.py     # Test calculations logic
├── bootstrap_db.py     # Database initialization
├── requirements.txt    # Python dependencies
│
├── /templates          # HTML templates (Jinja2)
│   ├── base.html       # Base layout template
│   ├── dashboard.html  # Dashboard home page
│   ├── projects.html   # Project listing
│   ├── samples.html    # Sample listing
│   ├── login.html      # Login page
│   └── ...
│
├── /static
│   └── style.css       # Custom CSS styles
│
└── /instance           # Instance folder (created at runtime)
    └── lims_dev.db     # SQLite database
```

## Main Features

### User Roles & Permissions

1. **Admin**
   - Create/edit/delete projects
   - Create/edit/delete samples
   - Create/edit/delete users
   - View audit logs

2. **Lab Technician**
   - Create/edit samples
   - Create/edit tests
   - View projects and samples

3. **Engineer**
   - View projects and samples
   - Approve/reject test results
   - Generate reports

### Core Modules

#### Projects Management
- Create, edit, and delete projects
- Track project status (Active, Completed, On Hold)
- Associate samples with projects

#### Sample Registration
- Register concrete, soil, and aggregate samples
- Link samples to projects
- Track collection date and client information

#### Test Management
- Assign tests to samples
- Calculate test results automatically
- Track test status and approval

#### Reports
- Export samples to Excel
- Export test results
- Generate PDF reports

## Useful Scripts

### Run Development Server
```powershell
python app.py
```

### Run Tests
```powershell
pytest tests/
```

### Run Database Bootstrap
```powershell
python bootstrap_db.py
```

### Generate Sample Data
```powershell
python scripts/generate_examples.py
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to 5001 or another port
```

### Database Connection Error
- Check `.env` file configuration
- For SQLite: Ensure `instance/` folder exists
- For MySQL: Verify server is running and credentials are correct

### Missing Templates
- Ensure all HTML files are in `/templates` folder
- Check file names match exactly (case-sensitive on Linux)

### Module Import Errors
```powershell
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Development Mode

The application runs in debug mode by default, which provides:
- Auto-reloading when files change
- Detailed error pages
- Interactive debugger

## Production Deployment

For production use:
1. Set `debug=False` in `app.py`
2. Use a production database (MySQL/PostgreSQL)
3. Set strong `SECRET_KEY`
4. Use a WSGI server (Gunicorn, uWSGI)
5. Configure HTTPS/SSL
6. Set up proper logging

## Database Backup

```powershell
# For SQLite
Copy-Item .\instance\lims_dev.db .\backups\lims_dev_backup.db

# For MySQL
mysqldump -u user -p lims_db > backup.sql
```

## Support

For issues or questions:
1. Check the README.md file
2. Review the QUICK_REFERENCE.md file
3. Check application logs in console output
4. Review test files in `/tests` folder

---
**Last Updated**: December 2025
