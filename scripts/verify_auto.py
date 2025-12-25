from auto_calculations import process_readings

# Test 1: compressive + sieve
readings1 = {
    'compressive': {'load_kN': 250.0, 'area_mm2': 19600},
    'sieve': {
        'sieve_masses': {75:10, 37.5:20, 19:30, 9.5:25, 4.75:10},
        'total_mass': 95.0
    }
}

res1 = process_readings(readings1)
assert 'compressive_strength_mpa' in res1
assert abs(res1['compressive_strength_mpa'] - 12.755102040816327) < 1e-6
assert 'sieve_analysis' in res1
print('verify_auto: test1 OK')

# Test 2: atterberg + proctor
readings2 = {
    'atterberg': {'liquid_limit': 45.0, 'plastic_limit': 18.0},
    'proctor': {'dry_density_kgm3': 2000.0, 'water_content_percent': 12.5}
}

res2 = process_readings(readings2)
assert 'atterberg' in res2 and res2['atterberg']['PI'] == 27.0
assert 'proctor' in res2 and res2['proctor']['dry_density'] == 2000.0
print('verify_auto: test2 OK')

print('All verification checks passed')
