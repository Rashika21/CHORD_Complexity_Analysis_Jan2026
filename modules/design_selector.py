"""
Design Selector
===============
Select 4 representative designs for detailed analysis.
Based on PDF document specifications:
- Design 1: Least Complexity
- Design 14: Medium Complexity
- Design 5: Highest Complexity
- Design 12: Non-Classical Complexity
"""

from typing import Dict, List, Tuple
from collections import Counter
import networkx as nx
from .setup import get_design_number


def select_representative_designs(all_designs_data: Dict, 
                                 specific_designs: Dict[str, int] = None) -> List[Tuple[str, Dict]]:
    """
    Select 4 representative designs for detailed analysis.
    
    Parameters:
    -----------
    all_designs_data : dict
        All design data from load_all_designs()
    specific_designs : dict, optional
        Dictionary mapping labels to design numbers.
        Default: {'Least Complexity': 1, 'Medium Complexity': 14, 
                 'Highest Complexity': 5, 'Non-Classical': 12}
    
    Returns:
    --------
    list
        List of (label, stats) tuples for selected designs
    """
    if specific_designs is None:
        specific_designs = {
            'Least Complexity': 1,
            'Medium Complexity': 14,
            'Highest Complexity': 5,
            'Most Uncertain/Non-Classical': 12
        }
    
    # Get sorted design names
    sorted_design_names = sorted(all_designs_data.keys(), key=get_design_number)
    
    # Find designs by number
    design_by_number = {}
    for design_name in sorted_design_names:
        num = get_design_number(design_name)
        design_by_number[num] = design_name
    
    selected_designs = []
    
    for label, design_num in specific_designs.items():
        if design_num in design_by_number:
            design_name = design_by_number[design_num]
            design_data = all_designs_data[design_name]
            G = design_data['G']
            payload = design_data['payload']
            
            # Calculate statistics
            connections = payload.get('connections', [])
            edge_set = set()
            for conn in connections:
                from_ci = conn.get('from_ci')
                to_ci = conn.get('to_ci')
                if from_ci and to_ci:
                    edge_set.add((from_ci, to_ci))
            
            # Count directed and bidirectional
            directed_count = 0
            bidirectional_count = 0
            for conn in connections:
                from_ci = conn.get('from_ci')
                to_ci = conn.get('to_ci')
                if from_ci and to_ci:
                    if (to_ci, from_ci) in edge_set:
                        bidirectional_count += 1
                    else:
                        directed_count += 1
            
            reciprocal = bidirectional_count // 2
            one_way = directed_count
            
            # Component type diversity
            comp_types = list(nx.get_node_attributes(G, "component_type").values())
            type_counts = Counter(comp_types)
            type_diversity = len(type_counts)
            
            # Connection type diversity
            conn_types = []
            for u, v, attrs in G.edges(data=True):
                conn_type = f"{attrs.get('from_conn', '')}→{attrs.get('to_conn', '')}"
                conn_types.append(conn_type)
            conn_diversity = len(set(conn_types))
            
            # Uncertainty score
            uncertainty_score = type_diversity + conn_diversity + (reciprocal / max(len(G.edges()), 1))
            
            stats = {
                'design_name': design_name,
                'design_number': design_num,
                'num_nodes': G.number_of_nodes(),
                'num_edges': G.number_of_edges(),
                'type_diversity': type_diversity,
                'conn_diversity': conn_diversity,
                'reciprocal': reciprocal,
                'one_way': one_way,
                'uncertainty_score': uncertainty_score,
                'G': G,
                'payload': payload
            }
            
            selected_designs.append((label, stats))
        else:
            print(f"⚠ Warning: Design {design_num} not found for {label}")
    
    return selected_designs


def print_selected_designs(selected_designs: List[Tuple[str, Dict]], verbose: bool = True):
    """
    Print information about selected designs.
    
    Parameters:
    -----------
    selected_designs : list
        List of (label, stats) tuples
    verbose : bool
        Print detailed information (default: True)
    """
    if not verbose:
        return
    
    print("\n" + "=" * 80)
    print("SELECTED 4 REPRESENTATIVE DESIGNS")
    print("=" * 80)
    
    for label, stats in selected_designs:
        print(f"\n{label}:")
        print(f"  Design: {stats['design_name']} (Design {stats['design_number']})")
        print(f"  Nodes: {stats['num_nodes']}")
        print(f"  Edges: {stats['num_edges']}")
        print(f"  Component Types: {stats['type_diversity']}")
        print(f"  Connection Types: {stats['conn_diversity']}")
        print(f"  Reciprocal Pairs: {stats['reciprocal']}")
        print(f"  One-way Edges: {stats['one_way']}")
        if label == 'Most Uncertain/Non-Classical':
            print(f"  Uncertainty Score: {stats['uncertainty_score']:.2f}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    from .data_loader import load_all_designs
    
    # Test design selection
    design_dirs = get_sorted_designs(DATA_ROOT)
    all_designs_data = load_all_designs(design_dirs, verbose=False)
    selected_designs = select_representative_designs(all_designs_data)
    print_selected_designs(selected_designs)
