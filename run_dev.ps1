# run_dev.ps1 - Create venv, install requirements, and run the Flask dev server
# Usage: Open PowerShell, cd to project root (g:\lims), then:
#   .\run_dev.ps1

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python .\app.py
