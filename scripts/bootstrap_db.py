r"""bootstrap_db.py

Enhanced bootstrap helper to execute `schema.sql` against a MySQL server and
insert/update a default admin user. This version supports three input methods:

1) Provide full `DATABASE_URI` in `.env` or environment.
2) Provide CLI args: --uri OR --user/--host/--port/--db/--password.
3) Interactive prompt fallback (secure password via getpass).

Usage examples (PowerShell):
  # Use .env (already written):
  python .\scripts\bootstrap_db.py

  # Provide full URI on command line:
  python .\scripts\bootstrap_db.py --uri "mysql+pymysql://user:pass@host:3306/lims_db"

  # Provide parts on command line (password will be used as provided):
  python .\scripts\bootstrap_db.py --user dbuser --host dbhost --db lims_db

  # Non-interactive CI: pass --uri or set DATABASE_URI env var.
"""

import os
import sys
import argparse
import urllib.parse
import getpass
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


load_dotenv()

def build_uri_from_parts(user, password, host, port, dbname, driver='mysql+pymysql'):
    user_enc = urllib.parse.quote_plus(user)
    pwd_enc = urllib.parse.quote_plus(password)
    host = host or 'localhost'
    port = port or '3306'
    return f"{driver}://{user_enc}:{pwd_enc}@{host}:{port}/{dbname}"


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


def parse_args():
    parser = argparse.ArgumentParser(description='Bootstrap LIMS schema and admin user')
    parser.add_argument('--uri', help='Full SQLAlchemy DATABASE_URI (e.g. mysql+pymysql://user:pass@host:3306/db)')
    parser.add_argument('--user', help='DB user (used to build URI if --uri omitted)')
    parser.add_argument('--password', help='DB password (used to build URI if --uri omitted)')
    parser.add_argument('--host', help='DB host (default: localhost)')
    parser.add_argument('--port', help='DB port (default: 3306)')
    parser.add_argument('--db', help='DB name')
    parser.add_argument('--admin-user', help='Admin username to create/update (overrides .env)', default=None)
    parser.add_argument('--admin-pass', help='Admin password (overrides .env)', default=None)
    parser.add_argument('--no-prompt', action='store_true', help='Do not prompt interactively; fail if not enough info')
    return parser.parse_args()


def main():
    # 1) Try CLI args
    args = parse_args()

    # 2) Environment (.env)
    env_uri = os.getenv('DATABASE_URI')
    env_admin_user = os.getenv('ADMIN_USER', 'admin')
    env_admin_pass = os.getenv('ADMIN_PASS', 'admin')
    env_admin_role = os.getenv('ADMIN_ROLE', 'Admin')

    DATABASE_URI = None
    ADMIN_USER = args.admin_user or env_admin_user
    ADMIN_PASS = args.admin_pass or env_admin_pass
    ADMIN_ROLE = env_admin_role

    if args.uri:
        DATABASE_URI = args.uri

    # If no full URI, but user provided parts on CLI, build it
    if not DATABASE_URI and args.user and args.db:
        password = args.password
        if not password and not args.no_prompt:
            password = getpass.getpass('DB password (will not echo): ')
        if password is None:
            print('DB password required to build URI. Aborting.')
            return
        DATABASE_URI = build_uri_from_parts(args.user, password, args.host or 'localhost', args.port or '3306', args.db)

    # If still no URI, try env
    if not DATABASE_URI:
        if env_uri:
            DATABASE_URI = env_uri

    # If still no URI and prompting is allowed, prompt interactively
    if not DATABASE_URI:
        if args.no_prompt:
            print('No DATABASE_URI specified and interactive prompting disabled. Aborting.')
            return
        print('DATABASE_URI not set; entering interactive prompt to build connection string.')
        host = input('DB host (default: localhost): ') or 'localhost'
        port = input('DB port (default: 3306): ') or '3306'
        dbname = input('DB name: ').strip()
        if not dbname:
            print('DB name is required. Aborting.')
            return
        dbuser = input('DB user: ').strip()
        if not dbuser:
            print('DB user is required. Aborting.')
            return
        dbpass = getpass.getpass('DB password (hidden): ')
        DATABASE_URI = build_uri_from_parts(dbuser, dbpass, host, port, dbname)

    if not DATABASE_URI:
        print('DATABASE_URI not provided. Aborting.')
        return

    try:
        url = make_url(DATABASE_URI)
        print(f'Connecting to: {url.drivername}://{url.host or "localhost"}')
    except Exception:
        print('Provided DATABASE_URI appears invalid. Aborting.')
        return

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
