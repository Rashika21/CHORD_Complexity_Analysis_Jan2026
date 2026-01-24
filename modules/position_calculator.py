"""
Position Calculator
===================
Calculate 3D positions for network visualization that mimic actual CAD placement.
"""

import math
import numpy as np
import networkx as nx


def calculate_realistic_3d_positions(G, design_dir, geometry, payload):
    """
    Calculate 3D positions that mimic actual CAD model placement.
    
    Parameters:
    -----------
    G : networkx.MultiDiGraph
        Network graph
    design_dir : Path
        Design directory
    geometry : dict
        Geometry information from design tree
    payload : dict
        Design payload data
        
    Returns:
    --------
    dict
        Dictionary mapping node names to (x, y, z) positions
    """
    pos_3d = {}
    
    if not geometry:
        print(f"  ⚠ No geometry for {design_dir.name}, using fallback")
        pos_2d = nx.spring_layout(G, seed=hash(design_dir.name) % (2**32), k=0.7)
        return {node: (*coords, 0) for node, coords in pos_2d.items()}
    
    # Find hub node
    hub_node = None
    for node in G.nodes():
        if 'MainHub' in node:
            hub_node = node
            break
    
    if not hub_node:
        print(f"  ⚠ No hub found for {design_dir.name}")
        pos_2d = nx.spring_layout(G, seed=hash(design_dir.name) % (2**32), k=0.7)
        return {node: (*coords, 0) for node, coords in pos_2d.items()}
    
    # Hub at center, slightly above ground
    hub_z = 50
    center = (0, 0, hub_z)
    pos_3d[hub_node] = center
    
    num_arms = geometry.get('num_arms', 4)
    arm_length = geometry.get('arm_length', 400.0)
    angles = [2 * math.pi * i / num_arms for i in range(num_arms)]
    
    # Find arms connected to hub
    arms = []
    for edge in G.edges(data=True):
        u, v, attrs = edge
        if u == hub_node and 'Side_Connector' in str(attrs.get('from_conn', '')):
            arms.append((v, attrs.get('from_conn', '')))
        elif v == hub_node and 'Side_Connector' in str(attrs.get('to_conn', '')):
            arms.append((u, attrs.get('to_conn', '')))
    
    def get_connector_num(conn_str):
        """Extract connector number from connection string."""
        digits = ''.join(filter(str.isdigit, str(conn_str)))
        return int(digits) if digits else 999
    
    arms_sorted = sorted(arms, key=lambda x: get_connector_num(x[1]))
    
    # Position each arm and components
    for i, (arm_node, connector) in enumerate(arms_sorted[:num_arms]):
        angle = angles[i % len(angles)]
        arm_end_x = center[0] + arm_length * math.cos(angle)
        arm_end_y = center[1] + arm_length * math.sin(angle)
        arm_end_z = center[2]
        
        arm_mid_x = center[0] + (arm_length * 0.6) * math.cos(angle)
        arm_mid_y = center[1] + (arm_length * 0.6) * math.sin(angle)
        pos_3d[arm_node] = (arm_mid_x, arm_mid_y, arm_end_z)
        
        # Traverse arm chain
        current_node = arm_node
        visited = {hub_node, arm_node}
        
        for step in range(10):
            found_next = False
            for edge in G.edges(data=True):
                u, v, attrs = edge
                if u == current_node and v not in visited:
                    next_node = v
                    visited.add(v)
                    found_next = True
                elif v == current_node and u not in visited:
                    next_node = u
                    visited.add(u)
                    found_next = True
                else:
                    continue
                
                if found_next:
                    if 'Flange' in next_node:
                        pos_3d[next_node] = (arm_end_x * 0.9, arm_end_y * 0.9, arm_end_z)
                    elif 'Motor' in next_node:
                        pos_3d[next_node] = (arm_end_x, arm_end_y, arm_end_z)
                    elif 'Propeller' in next_node:
                        pos_3d[next_node] = (arm_end_x, arm_end_y, arm_end_z + 60)
                    else:
                        offset = 0.7 + step * 0.05
                        pos_3d[next_node] = (arm_end_x * offset, arm_end_y * offset, arm_end_z)
                    
                    current_node = next_node
                    break
            
            if not found_next:
                break
    
    # Position fuselage
    fuselage_node = None
    for node in G.nodes():
        if 'Fuselage' in node:
            fuselage_node = node
            break
    
    if fuselage_node:
        fuselage_z = center[2] - (geometry.get('fuselage', {}).get('floorHeight', 8.75) or 8.75) - 20
        pos_3d[fuselage_node] = (center[0], center[1], fuselage_z)
        
        # Position sensors
        sensor_positions = geometry.get('sensor_positions', {})
        sensor_mapping = {
            'Battery': 'battery',
            'Sensor_1': 'rpm',
            'Sensor_2': 'autopilot',
            'Sensor_3': 'current',
            'Sensor_4': 'voltage',
            'Sensor_5': 'gps',
            'Sensor_6': 'vario',
        }
        
        for node in G.nodes():
            if 'Sensor' in node or ('Battery' in node and 'Controller' not in node):
                sensor_key = None
                for key in sensor_mapping:
                    if key in node:
                        sensor_key = sensor_mapping[key]
                        break
                
                if sensor_key and sensor_key in sensor_positions:
                    sx, sy = sensor_positions[sensor_key]
                    scale = 0.4
                    pos_3d[node] = (center[0] + sx * scale, center[1] + sy * scale, fuselage_z)
                else:
                    pos_3d[node] = (center[0], center[1], fuselage_z - 15)
    
    # Position remaining components
    for node in G.nodes():
        if node not in pos_3d:
            connected = [v for u, v in G.edges() if u == node] + [u for u, v in G.edges() if v == node]
            for conn in connected:
                if conn in pos_3d:
                    base_pos = pos_3d[conn]
                    pos_3d[node] = (
                        base_pos[0] + np.random.uniform(-30, 30),
                        base_pos[1] + np.random.uniform(-30, 30),
                        base_pos[2] + np.random.uniform(-20, 20)
                    )
                    break
            if node not in pos_3d:
                pos_3d[node] = (
                    center[0] + np.random.uniform(-80, 80),
                    center[1] + np.random.uniform(-80, 80),
                    center[2] + np.random.uniform(-40, 40)
                )
    
    return pos_3d


def calculate_all_positions(all_designs_data, designs_geometry, verbose=True):
    """
    Calculate 3D positions for all designs.
    
    Parameters:
    -----------
    all_designs_data : dict
        All design data
    designs_geometry : dict
        All design geometries
    verbose : bool
        Print progress
        
    Returns:
    --------
    dict
        Dictionary mapping design names to position dictionaries
    """
    if verbose:
        print("\n" + "=" * 80)
        print("CALCULATING REALISTIC 3D POSITIONS (CAD-MIMICKED)")
        print("=" * 80)
    
    all_positions_3d = {}
    
    for design_name, data in all_designs_data.items():
        geometry = designs_geometry.get(design_name)
        pos_3d = calculate_realistic_3d_positions(
            data['G'], 
            data['design_dir'], 
            geometry, 
            data['payload']
        )
        all_positions_3d[design_name] = pos_3d
        
        if verbose:
            print(f"✓ {design_name}: {len(pos_3d)} nodes positioned")
    
    if verbose:
        print(f"\n✓ Calculated positions for {len(all_positions_3d)} designs")
    
    return all_positions_3d


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    from .data_loader import load_all_designs
    from .geometry_parser import parse_all_geometries
    
    # Test position calculation
    design_dirs = get_sorted_designs(DATA_ROOT)
    all_designs_data = load_all_designs(design_dirs, verbose=False)
    designs_geometry = parse_all_geometries(all_designs_data, verbose=False)
    all_positions = calculate_all_positions(all_designs_data, designs_geometry)
    print(f"✓ Position calculation test completed")
