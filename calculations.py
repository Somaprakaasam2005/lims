"""
calculations.py - Auto calculation module for lab tests

Includes:
- compressive_strength_mpa(load_kN, area_mm2)
- flexural_strength_mpa(load_kN, length_mm, width_mm, depth_mm)
- split_tensile_strength_mpa(load_kN, length_mm, diameter_mm)
- water_absorption_percent(dry_mass_g, saturated_mass_g)
- cbr_value(load_at_penetration_kN, standard_load_kN)
- proctor_compaction(dry_density_kgm3, water_content_percent)
- sieve_analysis_summary(sieve_masses, total_mass)
- atterberg_limits(liquid_limit, plastic_limit)

The functions are simple, well-commented, and suitable for college demos.
"""
from typing import Dict, List, Any

def compressive_strength_mpa(load_kN: float, area_mm2: float) -> float:
    """
    Calculate compressive strength in MPa.

    Formula: Compressive Strength = Load / Area
    If load is provided in kN and area in mm^2, then:
      strength (MPa) = (load_kN * 1000 N/kN) / (area_mm2 N/mm^2) = N/mm^2 = MPa

    Args:
      load_kN: Load at failure in kilonewtons (kN)
      area_mm2: Cross sectional area in square millimeters (mm^2)

    Returns:
      Strength in MPa (float)
    """
    if area_mm2 <= 0:
        raise ValueError('Area must be positive')
    strength = (load_kN * 1000.0) / area_mm2
    return strength


def flexural_strength_mpa(load_kN: float, length_mm: float, width_mm: float, depth_mm: float) -> float:
    """
    Calculate flexural strength (modulus of rupture) for concrete beam in MPa.
    
    Formula for center-point loading (IS 516):
    fb = (P * L) / (b * d^2)
    
    Where:
    - fb = flexural strength (MPa)
    - P = maximum load (N)
    - L = span length (mm)
    - b = width of specimen (mm)
    - d = depth of specimen (mm)
    
    Args:
        load_kN: Maximum load at failure in kilonewtons (kN)
        length_mm: Span length between supports in millimeters (mm)
        width_mm: Width of beam specimen (mm)
        depth_mm: Depth of beam specimen (mm)
    
    Returns:
        Flexural strength in MPa (float)
    """
    if width_mm <= 0 or depth_mm <= 0 or length_mm <= 0:
        raise ValueError('Dimensions must be positive')
    
    load_N = load_kN * 1000.0  # Convert kN to N
    
    # Formula: fb = (P * L) / (b * d^2)
    # Result in N/mm^2 = MPa
    flexural_strength = (load_N * length_mm) / (width_mm * depth_mm * depth_mm)
    
    return flexural_strength


def split_tensile_strength_mpa(load_kN: float, length_mm: float, diameter_mm: float) -> float:
    """
    Calculate split tensile strength for concrete cylinder in MPa.
    
    Formula (IS 5816):
    T = (2 * P) / (π * L * D)
    
    Where:
    - T = split tensile strength (MPa)
    - P = maximum load (N)
    - L = length of cylinder (mm)
    - D = diameter of cylinder (mm)
    
    Args:
        load_kN: Maximum splitting load in kilonewtons (kN)
        length_mm: Length of cylinder (mm)
        diameter_mm: Diameter of cylinder (mm)
    
    Returns:
        Split tensile strength in MPa (float)
    """
    if length_mm <= 0 or diameter_mm <= 0:
        raise ValueError('Dimensions must be positive')
    
    import math
    load_N = load_kN * 1000.0
    
    # T = (2 * P) / (π * L * D)
    tensile_strength = (2.0 * load_N) / (math.pi * length_mm * diameter_mm)
    
    return tensile_strength


def water_absorption_percent(dry_mass_g: float, saturated_mass_g: float) -> float:
    """
    Calculate water absorption percentage for concrete/brick specimens.
    
    Formula:
    WA = ((Ws - Wd) / Wd) * 100
    
    Where:
    - WA = water absorption (%)
    - Ws = saturated surface dry mass (g)
    - Wd = oven dry mass (g)
    
    Args:
        dry_mass_g: Oven dry mass in grams
        saturated_mass_g: Saturated surface dry mass in grams
    
    Returns:
        Water absorption percentage (float)
    """
    if dry_mass_g <= 0:
        raise ValueError('Dry mass must be positive')
    if saturated_mass_g < dry_mass_g:
        raise ValueError('Saturated mass cannot be less than dry mass')
    
    absorption = ((saturated_mass_g - dry_mass_g) / dry_mass_g) * 100.0
    
    return absorption


def cbr_value(load_at_penetration_kN: float, standard_load_kN: float) -> float:
    """
    Calculate California Bearing Ratio (CBR) for soil.
    
    Formula:
    CBR = (Test Load / Standard Load) * 100
    
    Standard loads:
    - 2.5mm penetration: 13.24 kN
    - 5.0mm penetration: 19.96 kN
    
    Args:
        load_at_penetration_kN: Load at specified penetration (kN)
        standard_load_kN: Standard load for that penetration (13.24 or 19.96 kN)
    
    Returns:
        CBR value as percentage (float)
    """
    if standard_load_kN <= 0:
        raise ValueError('Standard load must be positive')
    
    cbr = (load_at_penetration_kN / standard_load_kN) * 100.0
    
    return cbr


def proctor_compaction(dry_density_kgm3: float, water_content_percent: float) -> Dict[str, float]:
    """
    Process Proctor compaction test data.
    
    Returns dry density and water content for plotting compaction curve.
    In practice, multiple data points are needed to find optimum moisture content (OMC)
    and maximum dry density (MDD).
    
    Args:
        dry_density_kgm3: Dry density in kg/m³
        water_content_percent: Water content in percent
    
    Returns:
        dict with 'dry_density' and 'water_content'
    """
    if dry_density_kgm3 <= 0:
        raise ValueError('Dry density must be positive')
    if water_content_percent < 0:
        raise ValueError('Water content cannot be negative')
    
    return {
        'dry_density': round(dry_density_kgm3, 2),
        'water_content': round(water_content_percent, 2)
    }


def _interpolate_d_value(sieve_sizes: List[float], percent_passing: List[float], target_percent: float) -> float:
    """
    Interpolate to find the particle size (D) corresponding to a target percent passing.
    Sieve sizes and percent_passing must be sorted in descending sieve size order.
    """
    # Find bracketing indices
    for i in range(1, len(percent_passing)):
        if percent_passing[i-1] >= target_percent >= percent_passing[i]:
            # Linear interpolation in log space for particle size is common, but for simplicity use linear here
            x1, x2 = percent_passing[i-1], percent_passing[i]
            d1, d2 = sieve_sizes[i-1], sieve_sizes[i]
            if x1 == x2:
                return d1
            frac = (target_percent - x1) / (x2 - x1)
            d = d1 + frac * (d2 - d1)
            return d
    return None


def sieve_analysis_summary(sieve_masses: Dict[float, float], total_mass: float) -> Dict[str, Any]:
    """
    Given a dictionary of sieve size -> mass retained and the total sample mass,
    compute percent retained and percent passing for each sieve and return a summary.

    Also interpolate D10, D30, D60 and compute coefficients Cu and Cc when possible.

    Args:
      sieve_masses: dict where keys are sieve sizes (e.g., 75, 37.5, 19, ...) and values are mass retained on that sieve
      total_mass: total dry mass of sample (g)

    Returns:
      dict with 'summary_table' (list of rows), 'D10', 'D30', 'D60', 'Cu', 'Cc'
    """
    if total_mass <= 0:
        raise ValueError('Total mass must be positive')

    # Sort sieve sizes descending (coarsest to finest)
    sizes = sorted(sieve_masses.keys(), reverse=True)
    table = []
    cumulative_retained = 0.0
    cum_percent_retained_list = []
    percent_passing_list = []

    for s in sizes:
        retained = sieve_masses.get(s, 0.0)
        percent_retained = (retained / total_mass) * 100.0
        cumulative_retained += percent_retained
        percent_passing = 100.0 - cumulative_retained
        table.append({'sieve_mm': s, 'retained_g': retained, 'percent_retained': round(percent_retained, 2), 'cumulative_retained': round(cumulative_retained,2), 'percent_passing': round(percent_passing,2)})
        cum_percent_retained_list.append(cumulative_retained)
        percent_passing_list.append(percent_passing)

    # Prepare arrays for interpolation: need percent passing corresponding to sieve sizes
    # percent_passing_list is already aligned with sizes
    D10 = D30 = D60 = None
    try:
        # We want to find size where percent passing equals 10,30,60
        D10 = _interpolate_d_value(sizes, percent_passing_list, 10.0)
        D30 = _interpolate_d_value(sizes, percent_passing_list, 30.0)
        D60 = _interpolate_d_value(sizes, percent_passing_list, 60.0)
    except Exception:
        D10 = D30 = D60 = None

    Cu = Cc = None
    if D10 and D60 and D10 > 0:
        try:
            Cu = D60 / D10
            Cc = (D30 ** 2) / (D10 * D60) if D30 else None
        except Exception:
            Cu = Cc = None

    return {
        'summary_table': table,
        'D10': D10,
        'D30': D30,
        'D60': D60,
        'Cu': Cu,
        'Cc': Cc
    }


def atterberg_limits(liquid_limit: float, plastic_limit: float) -> Dict[str, float]:
        """Compute Atterberg limits summary.

        For demonstration we compute:
            - Plasticity Index (PI) = Liquid Limit - Plastic Limit

        Args:
            liquid_limit: Liquid limit in percent
            plastic_limit: Plastic limit in percent

        Returns:
            dict with keys 'LL', 'PL', 'PI'
        """
        if liquid_limit < 0 or plastic_limit < 0:
                raise ValueError('Limits must be non-negative')
        pi = liquid_limit - plastic_limit
        return {'LL': round(liquid_limit, 2), 'PL': round(plastic_limit, 2), 'PI': round(pi, 2)}
