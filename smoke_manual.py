# Manual smoke test helper (do not run under pytest)
# Use this script interactively to exercise the running server.

import requests

BASE = 'http://127.0.0.1:5000'

s = requests.Session()
print('Login form: GET /login ->', s.get(BASE + '/login').status_code)
print('To perform full smoke test run run_and_test.py which starts server internally and runs automated checks.')
