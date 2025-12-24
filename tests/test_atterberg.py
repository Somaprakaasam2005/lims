from calculations import atterberg_limits


def test_atterberg_basic():
    summary = atterberg_limits(LL:=40.0, PL:=20.0)
    assert summary['LL'] == 40.0
    assert summary['PL'] == 20.0
    assert summary['PI'] == 20.0


def test_atterberg_invalid():
    try:
        atterberg_limits(-5, 10)
        assert False, 'expected ValueError for negative input'
    except ValueError:
        pass
