import math
from calculations import compressive_strength_mpa, sieve_analysis_summary

def test_compressive_strength():
    strength = compressive_strength_mpa(250.0, 19600)
    assert isinstance(strength, float)
    assert math.isclose(strength, 12.755102040816327, rel_tol=1e-6)

def test_sieve_analysis_basic():
    sieve_masses = {75:10, 37.5:20, 19:30, 9.5:25, 4.75:10}
    total = 95.0
    summary = sieve_analysis_summary(sieve_masses, total)
    assert 'summary_table' in summary
    table = summary['summary_table']
    assert len(table) == len(sieve_masses)
    total_percent_retained = sum(row['percent_retained'] for row in table)
    # allow small floating rounding differences
    assert abs(total_percent_retained - 100.0) < 1e-2
    assert 'D10' in summary and 'D30' in summary and 'D60' in summary
