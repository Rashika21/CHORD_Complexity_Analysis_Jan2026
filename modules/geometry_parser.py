"""
Geometry Parser
===============
Parse design tree to extract geometric information.
"""

from .setup import get_design_number


def parse_design_tree(design_tree):
    """
    Extract geometric information from design_tree.json.
    
    Parameters:
    -----------
    design_tree : dict
        Design tree JSON data
        
    Returns:
    --------
    dict or None
        Geometry information dictionary or None if parsing failed
    """
    if not design_tree:
        return None
    
    geometry = {
        'hub_type': design_tree.get('hub', {}).get('node_type', 'Unknown'),
        'arm_length': None,
        'num_arms': 4,
        'fuselage': {},
        'sensor_positions': {}
    }
    
    # Extract arm information
    main_segment = design_tree.get('hub', {}).get('mainSegment', {})
    if main_segment:
        geometry['arm_length'] = main_segment.get('armLength')
    
    # Detect number of arms from hub type
    if '4' in geometry['hub_type']:
        geometry['num_arms'] = 4
    elif '6' in geometry['hub_type']:
        geometry['num_arms'] = 6
    elif '8' in geometry['hub_type']:
        geometry['num_arms'] = 8
    
    # Extract fuselage information
    fuselage_data = design_tree.get('fuselageWithComponents', {}).get('fuselage', {})
    if fuselage_data:
        geometry['fuselage'] = {
            'length': fuselage_data.get('length', 100),
            'horzDiameter': fuselage_data.get('horzDiameter', 300),
            'vertDiameter': fuselage_data.get('vertDiameter', 50),
            'floorHeight': fuselage_data.get('floorHeight', 8.75),
        }
        geometry['sensor_positions'] = {
            'battery': (fuselage_data.get('batteryX', 0), fuselage_data.get('batteryY', 0)),
            'rpm': (fuselage_data.get('rpmX', 0), fuselage_data.get('rpmY', 0)),
            'autopilot': (fuselage_data.get('autoPilotX', 0), fuselage_data.get('autoPilotY', 0)),
            'current': (fuselage_data.get('currentX', 0), fuselage_data.get('currentY', 0)),
            'voltage': (fuselage_data.get('voltageX', 0), fuselage_data.get('voltageY', 0)),
            'gps': (fuselage_data.get('gpsX', 0), fuselage_data.get('gpsY', 0)),
            'vario': (fuselage_data.get('varioX', 0), fuselage_data.get('varioY', 0)),
        }
    
    # Fallback for arm length
    if geometry['arm_length'] is None:
        geometry['arm_length'] = 400.0
    
    return geometry


def parse_all_geometries(all_designs_data, verbose=True):
    """
    Parse geometry for all designs.
    
    Parameters:
    -----------
    all_designs_data : dict
        Dictionary of design data
    verbose : bool
        Print progress information
        
    Returns:
    --------
    dict
        Dictionary mapping design names to geometry data
    """
    if verbose:
        print("\n" + "=" * 80)
        print("PARSING DESIGN TREE FOR GEOMETRY")
        print("=" * 80)
    
    designs_geometry = {}
    sorted_design_names = sorted(all_designs_data.keys(), key=get_design_number)
    
    for design_name in sorted_design_names:
        design_data = all_designs_data[design_name]
        geometry = parse_design_tree(design_data['design_tree'])
        designs_geometry[design_name] = geometry
        
        if verbose:
            if geometry:
                print(f"✓ {design_name}: {geometry['hub_type']}, {geometry['num_arms']} arms, "
                      f"arm length: {geometry['arm_length']:.1f}mm")
            else:
                print(f"⚠ {design_name}: Could not parse geometry")
    
    if verbose:
        successful = sum(1 for g in designs_geometry.values() if g is not None)
        print(f"\n✓ Successfully parsed geometry for {successful}/{len(designs_geometry)} designs")
    
    return designs_geometry


def get_geometry_summary(designs_geometry):
    """
    Get summary statistics of geometries.
    
    Parameters:
    -----------
    designs_geometry : dict
        Dictionary of geometry data
        
    Returns:
    --------
    dict
        Summary statistics
    """
    hub_types = {}
    arm_counts = {}
    arm_lengths = []
    
    for design_name, geometry in designs_geometry.items():
        if geometry:
            # Count hub types
            hub_type = geometry['hub_type']
            hub_types[hub_type] = hub_types.get(hub_type, 0) + 1
            
            # Count arm numbers
            num_arms = geometry['num_arms']
            arm_counts[num_arms] = arm_counts.get(num_arms, 0) + 1
            
            # Collect arm lengths
            if geometry['arm_length']:
                arm_lengths.append(geometry['arm_length'])
    
    summary = {
        'hub_types': hub_types,
        'arm_counts': arm_counts,
        'arm_length_range': (min(arm_lengths), max(arm_lengths)) if arm_lengths else (0, 0),
        'arm_length_avg': sum(arm_lengths) / len(arm_lengths) if arm_lengths else 0,
    }
    
    return summary


def print_geometry_summary(designs_geometry):
    """Print summary of geometries."""
    summary = get_geometry_summary(designs_geometry)
    
    print("\n" + "=" * 80)
    print("GEOMETRY SUMMARY")
    print("=" * 80)
    print(f"Hub types:")
    for hub_type, count in sorted(summary['hub_types'].items()):
        print(f"  {hub_type}: {count}")
    print(f"\nArm configurations:")
    for num_arms, count in sorted(summary['arm_counts'].items()):
        print(f"  {num_arms} arms: {count} designs")
    print(f"\nArm lengths:")
    print(f"  Range: {summary['arm_length_range'][0]:.1f} - {summary['arm_length_range'][1]:.1f} mm")
    print(f"  Average: {summary['arm_length_avg']:.1f} mm")
    print("=" * 80)


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    from .data_loader import load_all_designs
    
    # Test geometry parsing
    design_dirs = get_sorted_designs(DATA_ROOT)
    all_designs_data = load_all_designs(design_dirs, verbose=False)
    designs_geometry = parse_all_geometries(all_designs_data)
    print_geometry_summary(designs_geometry)
