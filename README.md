Civil Engineering Laboratory LIMS (Simple College Project)

Overview

This is a simple web-based Laboratory Information Management System (LIMS) for civil engineering material testing labs. It's suitable for a college final-year project and demo.

Features

- User authentication (Admin, Lab Technician, Engineer)
- Sample management (Concrete, Soil, Aggregate)
- Test assignment and raw data input
- Automatic calculation for tests (e.g., compressive strength, sieve analysis)
- PDF report generation using ReportLab
- MySQL database via SQLAlchemy (PyMySQL)

Quick setup (Windows PowerShell)

1. Create a Python virtual environment and activate it:

`powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
`

2. Install dependencies:

`powershell
pip install -r requirements.txt
`

3. Configure database in a .env file at project root (example):

`
DATABASE_URI=mysql+pymysql://user:password@localhost/lims_db
SECRET_KEY=your-secret-key
`

4. Initialize database (run the SQL in schema.sql), or let SQLAlchemy create tables (adjust as needed).

5. Run the app:

`powershell
python app.py
`

Files

- pp.py - Flask entrypoint with routes and simple UI wiring.
- models.py - SQLAlchemy models mapping to MySQL tables.
- calculations.py - Concrete and soil calculation functions.
- eport_generator.py - ReportLab-based PDF generator.
- schema.sql - MySQL CREATE TABLE statements.
- sample_data.sql - Example data inserts for testing.
- 	emplates/ - HTML templates for login, dashboard, sample pages.
- static/ - CSS and client JS.

Notes

This project aims to be simple and well-commented for learning and viva. You can expand features (file upload, user management UI, more tests) after the demo.
