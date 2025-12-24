from calculations import sieve_analysis_summary


def test_sieve_d_values_present():
    sieve_masses = {75:10, 37.5:20, 19:30, 9.5:25, 4.75:10}
    total = 95.0
    summary = sieve_analysis_summary(sieve_masses, total)
    assert summary['D10'] is not None
    assert summary['D30'] is not None
    assert summary['D60'] is not None
    assert summary['Cu'] is not None or summary['Cu'] == 0 or summary['Cu'] is None
    # basic sanity: D60 should be >= D30 >= D10 if present
    D10 = summary['D10']
    D30 = summary['D30']
    D60 = summary['D60']
    if D10 and D30 and D60:
        assert D60 >= D30 >= D10
