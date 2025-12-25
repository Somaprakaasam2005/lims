"""
auto_calculations.py

Wrapper to process raw input readings and run appropriate calculation functions
so the user only needs to provide input readings and receives computed results.
"""
from typing import Dict, Any
import calculations


def process_readings(readings: Dict[str, Any]) -> Dict[str, Any]:
    """Process a dict of readings and return computed results.

    Supported keys in `readings`:
      - 'compressive': {'load_kN': float, 'area_mm2': float}
      - 'flexural': {'load_kN': float, 'length_mm': float, 'width_mm': float, 'depth_mm': float}
      - 'split_tensile': {'load_kN': float, 'length_mm': float, 'diameter_mm': float}
      - 'water_absorption': {'dry_mass_g': float, 'saturated_mass_g': float}
      - 'cbr': {'load_at_penetration_kN': float, 'standard_load_kN': float}
      - 'proctor': {'dry_density_kgm3': float, 'water_content_percent': float}
      - 'sieve': {'sieve_masses': dict, 'total_mass': float}
      - 'atterberg': {'liquid_limit': float, 'plastic_limit': float}

    Returns a dict mapping test name -> computed result (float or dict)
    """
    results: Dict[str, Any] = {}

    if 'compressive' in readings:
        r = readings['compressive']
        results['compressive_strength_mpa'] = calculations.compressive_strength_mpa(r['load_kN'], r['area_mm2'])

    if 'flexural' in readings:
        r = readings['flexural']
        results['flexural_strength_mpa'] = calculations.flexural_strength_mpa(r['load_kN'], r['length_mm'], r['width_mm'], r['depth_mm'])

    if 'split_tensile' in readings:
        r = readings['split_tensile']
        results['split_tensile_strength_mpa'] = calculations.split_tensile_strength_mpa(r['load_kN'], r['length_mm'], r['diameter_mm'])

    if 'water_absorption' in readings:
        r = readings['water_absorption']
        results['water_absorption_percent'] = calculations.water_absorption_percent(r['dry_mass_g'], r['saturated_mass_g'])

    if 'cbr' in readings:
        r = readings['cbr']
        results['cbr_percent'] = calculations.cbr_value(r['load_at_penetration_kN'], r['standard_load_kN'])

    if 'proctor' in readings:
        r = readings['proctor']
        results['proctor'] = calculations.proctor_compaction(r['dry_density_kgm3'], r['water_content_percent'])

    if 'sieve' in readings:
        r = readings['sieve']
        results['sieve_analysis'] = calculations.sieve_analysis_summary(r['sieve_masses'], r['total_mass'])

    if 'atterberg' in readings:
        r = readings['atterberg']
        results['atterberg'] = calculations.atterberg_limits(r['liquid_limit'], r['plastic_limit'])

    return results
