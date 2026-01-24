"""
Data Loader
===========
Load and parse UAV design data from JSON files.
"""

import json
import networkx as nx
from pathlib import Path
from .setup import get_design_number


def load_design_data(design_dir):
    """
    Load data for a single design.
    
    Parameters:
    -----------
    design_dir : Path
        Directory containing design files
        
    Returns:
    --------
    dict or None
        Dictionary with design data (payload, design_tree, graph, components)
        or None if loading failed
    """
    try:
        # Load design_low_level.json
        with open(design_dir / "design_low_level.json") as f:
            payload = json.load(f)
        
        # Load design_tree.json
        tree_path = design_dir / "design_tree.json"
        if tree_path.exists():
            with open(tree_path) as f:
                design_tree = json.load(f)
        else:
            design_tree = None
        
        # Build network graph
        components = {c["component_instance"]: c for c in payload["components"]}
        G = nx.MultiDiGraph(name=payload["name"])
        
        for name, attrs in components.items():
            G.add_node(name, 
                      component_type=attrs["component_type"],
                      component_choice=attrs["component_choice"])
        
        for conn in payload["connections"]:
            G.add_edge(conn["from_ci"], conn["to_ci"],
                      from_conn=conn["from_conn"],
                      to_conn=conn["to_conn"])
        
        return {
            'design_dir': design_dir,
            'design_name': design_dir.name,
            'payload': payload,
            'design_tree': design_tree,
            'G': G,
            'components': components,
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
        }
        
    except Exception as e:
        print(f"⚠ Error loading {design_dir.name}: {e}")
        return None


def load_all_designs(design_dirs, verbose=True):
    """
    Load all design data from a list of directories.
    
    Parameters:
    -----------
    design_dirs : list
        List of design directories (Path objects)
    verbose : bool
        Print progress information
        
    Returns:
    --------
    dict
        Dictionary mapping design names to design data
    """
    if verbose:
        print("\n" + "=" * 80)
        print("LOADING ALL DESIGN DATA")
        print("=" * 80)
    
    all_designs_data = {}
    
    # Process designs in ascending order
    for design_dir in design_dirs:
        data = load_design_data(design_dir)
        if data is not None:
            all_designs_data[design_dir.name] = data
            if verbose:
                print(f"✓ {design_dir.name}: {data['num_nodes']} nodes, {data['num_edges']} edges")
    
    if verbose:
        print(f"\n✓ Successfully loaded {len(all_designs_data)} designs")
    
    return all_designs_data


def get_design_stats(all_designs_data):
    """
    Get statistics for all loaded designs.
    
    Parameters:
    -----------
    all_designs_data : dict
        Design data dictionary
        
    Returns:
    --------
    dict
        Statistics summary
    """
    stats = {
        'num_designs': len(all_designs_data),
        'total_nodes': 0,
        'total_edges': 0,
        'avg_nodes': 0,
        'avg_edges': 0,
        'component_types': set(),
    }
    
    for design_name, data in all_designs_data.items():
        stats['total_nodes'] += data['num_nodes']
        stats['total_edges'] += data['num_edges']
        
        # Collect component types
        for node, attrs in data['G'].nodes(data=True):
            comp_type = attrs.get('component_type', 'Unknown')
            stats['component_types'].add(comp_type)
    
    if stats['num_designs'] > 0:
        stats['avg_nodes'] = stats['total_nodes'] / stats['num_designs']
        stats['avg_edges'] = stats['total_edges'] / stats['num_designs']
    
    return stats


def print_design_stats(all_designs_data):
    """Print statistics for loaded designs."""
    stats = get_design_stats(all_designs_data)
    
    print("\n" + "=" * 80)
    print("DESIGN DATA STATISTICS")
    print("=" * 80)
    print(f"Number of designs: {stats['num_designs']}")
    print(f"Total nodes:       {stats['total_nodes']}")
    print(f"Total edges:       {stats['total_edges']}")
    print(f"Average nodes:     {stats['avg_nodes']:.1f}")
    print(f"Average edges:     {stats['avg_edges']:.1f}")
    print(f"Component types:   {len(stats['component_types'])}")
    print(f"  Types: {', '.join(sorted(stats['component_types']))}")
    print("=" * 80)


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    
    # Test loading
    design_dirs = get_sorted_designs(DATA_ROOT)
    all_designs_data = load_all_designs(design_dirs)
    print_design_stats(all_designs_data)
