from calculations import flexural_strength_mpa


def test_flexural_strength_basic():
    """Test basic flexural strength calculation."""
    # Standard concrete beam: 45 kN load, 500mm span, 150mm width, 150mm depth
    load_kN = 45.0
    length_mm = 500.0
    width_mm = 150.0
    depth_mm = 150.0
    
    result = flexural_strength_mpa(load_kN, length_mm, width_mm, depth_mm)
    
    # Expected: (45000 * 500) / (150 * 150 * 150) = 22500000 / 3375000 = 6.67 MPa
    assert abs(result - 6.67) < 0.01, f"Expected ~6.67 MPa, got {result}"


def test_flexural_strength_zero_dimension():
    """Test that zero dimensions raise an error."""
    try:
        flexural_strength_mpa(45, 500, 0, 150)
        assert False, "Should raise ValueError for zero width"
    except ValueError as e:
        assert 'positive' in str(e).lower()


def test_flexural_strength_various_loads():
    """Test flexural strength with different loads."""
    # Keep dimensions constant, vary load
    length_mm = 450.0
    width_mm = 150.0
    depth_mm = 150.0
    
    # Load 30 kN
    result1 = flexural_strength_mpa(30, length_mm, width_mm, depth_mm)
    # Load 60 kN (double the load should double the strength)
    result2 = flexural_strength_mpa(60, length_mm, width_mm, depth_mm)
    
    assert abs(result2 - 2 * result1) < 0.01, "Strength should scale linearly with load"
