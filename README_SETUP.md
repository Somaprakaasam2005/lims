Quick setup (Windows PowerShell)

1. Create and activate a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. Run the app (SQLite dev DB will be used by default):

```powershell
python .\app.py
# Open http://127.0.0.1:5000 and login with admin / admin
```

3. Optional: Bootstrap a MySQL database

- Create a `.env` file with a DATABASE_URI, e.g.:

```
DATABASE_URI=mysql+pymysql://user:pass@localhost/lims_db
SECRET_KEY=your_secret_here
```

- Run the bootstrap script:

```powershell
python .\scripts\bootstrap_db.py
```

4. Run tests:

```powershell
python -m pytest -q
```
