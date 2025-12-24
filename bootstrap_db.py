"""
bootstrap_db.py

Simple helper to execute `schema.sql` against a MySQL server (from DATABASE_URI in .env)
and insert a default admin user with a hashed password.

Usage (PowerShell):
  # ensure .env has DATABASE_URI and optional ADMIN_USER, ADMIN_PASS
  python .\scripts\bootstrap_db.py

Notes:
- This script targets MySQL (mysql+pymysql). If you use SQLite for local dev, the Flask app
  already creates a default admin user on first run (see `app.py`).
"""
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'admin')
ADMIN_ROLE = os.getenv('ADMIN_ROLE', 'Admin')

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')


def execute_sql_file(engine, path):
    with open(path, 'r', encoding='utf-8') as f:
        sql = f.read()
    # Simple splitter by semicolon; ignore empty statements
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    with engine.begin() as conn:
        for stmt in statements:
            try:
                conn.execute(text(stmt))
            except Exception as e:
                # Print and continue - some statements (like USE) may behave differently
                print(f"Warning executing statement: {e}")


def main():
    if not DATABASE_URI:
        print('DATABASE_URI not set in environment (.env). Aborting.')
        return

    url = make_url(DATABASE_URI)
    print(f'Connecting to: {url.drivername}://{url.host or "localhost"}')

    if 'mysql' not in url.drivername:
        print('This bootstrap script currently supports MySQL (mysql+pymysql).')
        print('For SQLite/local dev, run the Flask app once (app.py) and it will create default admin if needed.')
        return

    engine = create_engine(DATABASE_URI, future=True)

    # Execute schema
    if os.path.exists(SCHEMA_FILE):
        print('Executing schema.sql...')
        execute_sql_file(engine, SCHEMA_FILE)
        print('Schema executed (or attempted).')
    else:
        print(f'schema.sql not found at {SCHEMA_FILE}. Skipping schema execution.')

    # Create / upsert admin user
    pwd_hash = generate_password_hash(ADMIN_PASS)
    insert_stmt = text("""
    INSERT INTO users (username, password_hash, role) 
    VALUES (:username, :password_hash, :role)
    ON DUPLICATE KEY UPDATE password_hash = :password_hash, role = :role
    """)
    try:
        with engine.begin() as conn:
            conn.execute(insert_stmt, {'username': ADMIN_USER, 'password_hash': pwd_hash, 'role': ADMIN_ROLE})
        print(f'Admin user "{ADMIN_USER}" created/updated.')
    except Exception as e:
        print(f'Error creating admin user: {e}')


if __name__ == '__main__':
    main()
