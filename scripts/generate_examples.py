"""Generate example samples and reports for different test types.

This script starts the Flask app in-process (so you don't need to manually run it)
and creates example samples and tests, then triggers report generation.

Run from project root:
    python scripts/generate_examples.py

The generated PDFs will be placed in the `reports/` directory.
"""
import sys
import os
# Ensure project root is importable when this script is run from the scripts/ folder
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from werkzeug.serving import make_server
from threading import Thread
import time
import requests
import app as myapp

BASE = 'http://127.0.0.1:5000'

server = make_server('127.0.0.1', 5000, myapp.app)
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()

# wait until server is up
for _ in range(20):
    try:
        r = requests.get(BASE + '/login', timeout=1)
        if r.status_code == 200:
            break
    except Exception:
        time.sleep(0.2)
else:
    print('Server did not start')
    server.shutdown()
    raise SystemExit(1)

s = requests.Session()
# login as default admin (app creates admin/admin in dev SQLite)
r = s.post(BASE + '/login', data={'username':'admin','password':'admin'})
if r.status_code not in (200,302):
    print('Login failed')
    server.shutdown()
    raise SystemExit(1)

# Example 1: Compressive strength
resp = s.post(BASE + '/samples/new', data={'sample_id':'EX-COMP-1','sample_type':'Concrete','project_name':'Proj','client_name':'C'})
r = s.get(BASE + '/samples')
import re
m = re.search(r"<tr>\s*<td>(\d+)</td>\s*<td>EX-COMP-1</td>", r.text)
if m:
    sid = m.group(1)
    s.post(f'{BASE}/samples/{sid}', data={'test_name':'Compressive Strength','raw_value':'300,19600'})
    # find test id then calc and report
    r2 = s.get(f'{BASE}/samples/{sid}').text
    mt = re.search(r"<td>(\d+)</td>\s*<td>Compressive Strength</td>", r2)
    if mt:
        tid = mt.group(1)
        s.get(f'{BASE}/calculate/compressive/{tid}')
        r3 = s.get(f'{BASE}/reports/generate/{tid}')
        open(f'reports/example_comp_{tid}.pdf','wb').write(r3.content)

# Example 2: Sieve analysis
resp = s.post(BASE + '/samples/new', data={'sample_id':'EX-SIEVE-1','sample_type':'Aggregate','project_name':'Proj','client_name':'C'})
r = s.get(BASE + '/samples')
m = re.search(r"<tr>\s*<td>(\d+)</td>\s*<td>EX-SIEVE-1</td>", r.text)
if m:
    sid = m.group(1)
    # mass retained per sieve; total optional
    raw = '75:5;37.5:15;19:30;9.5:25;4.75:10;total:85'
    s.post(f'{BASE}/samples/{sid}', data={'test_name':'Sieve Analysis','raw_value':raw})
    r2 = s.get(f'{BASE}/samples/{sid}').text
    mt = re.search(r"<td>(\d+)</td>\s*<td>Sieve Analysis</td>", r2)
    if mt:
        tid = mt.group(1)
        s.get(f'{BASE}/calculate/sieve/{tid}')
        r3 = s.get(f'{BASE}/reports/generate/{tid}')
        open(f'reports/example_sieve_{tid}.pdf','wb').write(r3.content)

# Example 3: Atterberg limits
        resp = s.post(BASE + '/samples/new', data={'sample_id':'EX-ATB-1','sample_type':'Soil','project_name':'Proj','client_name':'C'})
        r = s.get(BASE + '/samples')
        m = re.search(r"<tr>\s*<td>(\d+)</td>\s*<td>EX-ATB-1</td>", r.text)
        if m:
            sid = m.group(1)
            # store LL and PL as raw values separated by comma: 'LL,PL'
            s.post(f'{BASE}/samples/{sid}', data={'test_name':'Atterberg Limits','raw_value':'40,20'})
            r2 = s.get(f'{BASE}/samples/{sid}').text
            mt = re.search(r"<td>(\d+)</td>\s*<td>Atterberg Limits</td>", r2)
            if mt:
                tid = mt.group(1)
                # For Atterberg we don't need a separate calculation endpoint; generate report directly
                r3 = s.get(f'{BASE}/reports/generate/{tid}')
                open(f'reports/example_atterberg_{tid}.pdf','wb').write(r3.content)

print('Examples generated in reports/')
server.shutdown()
thread.join()
