import re
import time
import requests
import os
from pathlib import Path
from threading import Thread


def main() -> None:
    """Run the smoke/functional test against the local Flask app.

    The procedural code was previously executed at import time which caused
    pytest collection to run the script and fail. Moving it under `main()`
    prevents execution during import.
    """
    # Set up environment for SQLite dev database before importing app
    os.environ.setdefault('DATABASE_URI', 'sqlite:///lims_dev.db')
    os.environ.setdefault('SECRET_KEY', 'dev-secret-for-testing')

    # Create and run the Flask app using werkzeug make_server so we can start it in background
    from werkzeug.serving import make_server
    import app as myapp

    SAVE_DIR = Path('reports')
    SAVE_DIR.mkdir(exist_ok=True)

    server = make_server('127.0.0.1', 5000, myapp.app)
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    print('Starting server...')
    thread.start()
    # give it a moment
    for i in range(10):
        try:
            r = requests.get('http://127.0.0.1:5000/login', timeout=1)
            print('Server responds', r.status_code)
            break
        except Exception:
            time.sleep(0.3)
    else:
        print('Server did not start in time')
        server.shutdown()
        raise SystemExit(1)

    s = requests.Session()
    BASE = 'http://127.0.0.1:5000'

    print('Logging in as admin/admin...')
    r = s.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin'})
    if r.status_code not in (200, 302):
        print('Login failed, status', r.status_code)
        print(r.text[:500])
        server.shutdown()
        raise SystemExit(1)
    print('Logged in.')

    # Register a new sample
    sample_code = 'SMOKE-API-001'
    print('Registering sample', sample_code)
    resp = s.post(f'{BASE}/samples/new', data={
        'sample_id': sample_code,
        'sample_type': 'Concrete',
        'project_name': 'SmokeAPI',
        'client_name': 'ClientAPI',
        'date_collected': ''
    })
    # Now fetch samples and find our sample id
    r = s.get(f'{BASE}/samples')
    html = r.text
    m = re.search(rf"<tr>\s*<td>(\d+)</td>\s*<td>{re.escape(sample_code)}</td>", html)
    if not m:
        print('Could not find created sample in /samples page')
        print(html[:1000])
        server.shutdown()
        raise SystemExit(1)
    sample_id = m.group(1)
    print('Sample created with id', sample_id)

    # Add compressive strength test
    print('Adding Compressive Strength test')
    resp = s.post(f'{BASE}/samples/{sample_id}', data={'test_name': 'Compressive Strength', 'raw_value': '250,19600'})
    # fetch sample page and find test id
    r = s.get(f'{BASE}/samples/{sample_id}')
    html = r.text
    m = re.search(r"<td>(\d+)</td>\s*<td>Compressive Strength</td>\s*<td>250,19600</td>", html)
    if not m:
        print('Could not find created test in sample detail')
        print(html[:1000])
        server.shutdown()
        raise SystemExit(1)
    test_id = m.group(1)
    print('Test created with id', test_id)

    # Trigger calculation
    print('Calculating compressive strength...')
    resp = s.get(f'{BASE}/calculate/compressive/{test_id}')
    if resp.status_code not in (200, 302):
        print('Calculate endpoint failed', resp.status_code)
        print(resp.text[:500])
        server.shutdown()
        raise SystemExit(1)
    print('Calculation triggered.')

    # Generate report and download PDF
    print('Generating PDF report...')
    resp = s.get(f'{BASE}/reports/generate/{test_id}')
    if resp.status_code != 200 or 'pdf' not in (resp.headers.get('Content-Type', '').lower()):
        print('Report generation failed, status', resp.status_code, 'content-type', resp.headers.get('Content-Type'))
        print(resp.text[:500])
        server.shutdown()
        raise SystemExit(1)
    file_path = SAVE_DIR / f'report_api_{test_id}.pdf'
    with open(file_path, 'wb') as f:
        f.write(resp.content)
    print('Report saved to', file_path.resolve())
    print('Smoke test completed successfully.')

    # Shutdown server
    server.shutdown()
    thread.join(timeout=2)
    print('Server shut down.')


if __name__ == '__main__':
    main()
