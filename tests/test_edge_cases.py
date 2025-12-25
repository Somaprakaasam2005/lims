import pytest

from calculations import (
    compressive_strength_mpa,
    flexural_strength_mpa,
    split_tensile_strength_mpa,
    water_absorption_percent,
    cbr_value,
    proctor_compaction,
    sieve_analysis_summary,
    atterberg_limits,
)
from auto_calculations import process_readings


def test_compressive_area_zero_raises():
    with pytest.raises(ValueError):
        compressive_strength_mpa(100.0, 0.0)


def test_flexural_invalid_dimensions_raises():
    with pytest.raises(ValueError):
        flexural_strength_mpa(10.0, 0.0, 100.0, 100.0)


def test_split_tensile_invalid_dimensions_raises():
    with pytest.raises(ValueError):
        split_tensile_strength_mpa(10.0, -10.0, 150.0)


def test_water_absorption_invalid_values():
    with pytest.raises(ValueError):
        water_absorption_percent(0.0, 10.0)
    with pytest.raises(ValueError):
        water_absorption_percent(100.0, 50.0)  # saturated < dry


def test_cbr_zero_standard_raises():
    with pytest.raises(ValueError):
        cbr_value(5.0, 0.0)


def test_proctor_negative_water_raises():
    with pytest.raises(ValueError):
        proctor_compaction(1800.0, -0.1)


def test_sieve_total_mass_zero_raises():
    with pytest.raises(ValueError):
        sieve_analysis_summary({75: 10, 37.5: 5}, 0.0)


def test_sieve_interpolation_no_bracket_returns_none():
    # If all percent_passing remain the same (e.g., 100%), D10/D30/D60 should be None
    sieves = {75: 0.0, 37.5: 0.0, 19: 0.0}
    summary = sieve_analysis_summary(sieves, 100.0)
    assert summary['D10'] is None
    assert summary['D30'] is None
    assert summary['D60'] is None


def test_atterberg_negative_raises():
    with pytest.raises(ValueError):
        atterberg_limits(-5.0, 10.0)


def test_auto_calculations_missing_field_raises_keyerror():
    # Missing 'area_mm2' should raise KeyError from wrapper
    readings = {'compressive': {'load_kN': 100.0}}
    with pytest.raises(KeyError):
        process_readings(readings)
