import math
from auto_calculations import process_readings


def test_process_compressive_and_sieve():
    readings = {
        'compressive': {'load_kN': 250.0, 'area_mm2': 19600},
        'sieve': {
            'sieve_masses': {75:10, 37.5:20, 19:30, 9.5:25, 4.75:10},
            'total_mass': 95.0
        }
    }

    results = process_readings(readings)

    assert 'compressive_strength_mpa' in results
    assert math.isclose(results['compressive_strength_mpa'], 12.755102040816327, rel_tol=1e-6)

    assert 'sieve_analysis' in results
    summary = results['sieve_analysis']
    assert 'summary_table' in summary
    table = summary['summary_table']
    assert len(table) == 5


def test_process_atterberg_and_proctor():
    readings = {
        'atterberg': {'liquid_limit': 45.0, 'plastic_limit': 18.0},
        'proctor': {'dry_density_kgm3': 2000.0, 'water_content_percent': 12.5}
    }

    results = process_readings(readings)

    assert 'atterberg' in results
    assert results['atterberg']['PI'] == 27.0

    assert 'proctor' in results
    assert results['proctor']['dry_density'] == 2000.0
