import re
import requests
from pathlib import Path

BASE = 'http://127.0.0.1:5000'
SAVE_DIR = Path('reports')
SAVE_DIR.mkdir(exist_ok=True)

s = requests.Session()

print('Logging in as admin/admin...')
r = s.post(f'{BASE}/login', data={'username':'admin','password':'admin'})
if r.status_code not in (200,302):
    print('Login failed, status', r.status_code)
    print(r.text[:500])
    raise SystemExit(1)
print('Logged in.')

# Register a new sample
sample_code = 'SMOKE-001'
print('Registering sample', sample_code)
resp = s.post(f'{BASE}/samples/new', data={
    'sample_id': sample_code,
    'sample_type': 'Concrete',
    'project_name': 'SmokeProject',
    'client_name': 'ClientA',
    'date_collected': ''
})
# Now fetch samples and find our sample id
r = s.get(f'{BASE}/samples')
html = r.text
m = re.search(rf"<tr>\s*<td>(\d+)</td>\s*<td>{re.escape(sample_code)}</td>", html)
if not m:
    print('Could not find created sample in /samples page')
    print(html[:1000])
    raise SystemExit(1)
sample_id = m.group(1)
print('Sample created with id', sample_id)

# Open sample detail and add a compressive strength test
print('Adding Compressive Strength test')
resp = s.post(f'{BASE}/samples/{sample_id}', data={'test_name':'Compressive Strength','raw_value':'250,19600'})
# fetch sample page and find test id
r = s.get(f'{BASE}/samples/{sample_id}')
html = r.text
m = re.search(r"<td>(\d+)</td>\s*<td>Compressive Strength</td>\s*<td>250,19600</td>", html)
if not m:
    print('Could not find created test in sample detail')
    print(html[:1000])
    raise SystemExit(1)
test_id = m.group(1)
print('Test created with id', test_id)

# Trigger calculation
print('Calculating compressive strength...')
resp = s.get(f'{BASE}/calculate/compressive/{test_id}')
if resp.status_code not in (200,302):
    print('Calculate endpoint failed', resp.status_code)
    print(resp.text[:500])
    raise SystemExit(1)
print('Calculation triggered.')

# Generate report and download PDF
print('Generating PDF report...')
resp = s.get(f'{BASE}/reports/generate/{test_id}')
if resp.status_code != 200 or resp.headers.get('Content-Type','').lower().find('pdf') == -1:
    print('Report generation failed, status', resp.status_code, 'content-type', resp.headers.get('Content-Type'))
    print(resp.text[:500])
    raise SystemExit(1)
file_path = SAVE_DIR / f'report_test_{test_id}.pdf'
with open(file_path, 'wb') as f:
    f.write(resp.content)
print('Report saved to', file_path.resolve())
print('Smoke test completed successfully.')
