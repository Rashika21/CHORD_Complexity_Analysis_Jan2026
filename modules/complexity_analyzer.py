"""
Complexity Analyzer
===================
Calculate node and system complexity.
"""

import numpy as np
import networkx as nx
from collections import Counter


def shannon_entropy(probabilities):
    """
    Calculate Shannon entropy: H = -Σ(p_i * log2(p_i))
    
    Parameters:
    -----------
    probabilities : numpy array
        Array of probabilities (must sum to 1)
    
    Returns:
    --------
    float
        Shannon entropy value
    """
    # Remove zeros to avoid log(0)
    probs = probabilities[probabilities > 0]
    if len(probs) == 0:
        return 0.0
    return -np.sum(probs * np.log2(probs))


def calculate_system_entropies(G, payload):
    """
    Calculate system-level entropy metrics.
    
    Parameters:
    -----------
    G : NetworkX graph
        The network graph
    payload : dict
        Design payload with components and connections
    
    Returns:
    --------
    dict
        System entropy metrics (diversity, flexibility, combinability)
    """
    # 1. Diversity (Hdiv): Component type distribution
    component_types = [attrs.get('component_type', 'Unknown') 
                      for node, attrs in G.nodes(data=True)]
    type_counts = Counter(component_types)
    total_components = len(component_types)
    type_probs = np.array([count / total_components for count in type_counts.values()])
    H_div = shannon_entropy(type_probs)
    
    # 2. Flexibility (Hflex): Connection type diversity
    conn_types = []
    for conn in payload['connections']:
        conn_types.append(conn.get('from_conn', 'Unknown'))
        conn_types.append(conn.get('to_conn', 'Unknown'))
    conn_counts = Counter(conn_types)
    total_conns = len(conn_types)
    conn_probs = np.array([count / total_conns for count in conn_counts.values()])
    H_flex = shannon_entropy(conn_probs)
    
    # 3. Combinability (Hcomb): Degree distribution
    degrees = [G.degree(node) for node in G.nodes()]
    degree_counts = Counter(degrees)
    total_nodes = len(degrees)
    degree_probs = np.array([count / total_nodes for count in degree_counts.values()])
    H_comb = shannon_entropy(degree_probs)
    
    # 4. In-degree entropy
    in_degrees = [G.in_degree(node) for node in G.nodes()]
    in_degree_counts = Counter(in_degrees)
    in_degree_probs = np.array([count / total_nodes for count in in_degree_counts.values()])
    H_in = shannon_entropy(in_degree_probs)
    
    # 5. Out-degree entropy
    out_degrees = [G.out_degree(node) for node in G.nodes()]
    out_degree_counts = Counter(out_degrees)
    out_degree_probs = np.array([count / total_nodes for count in out_degree_counts.values()])
    H_out = shannon_entropy(out_degree_probs)
    
    return {
        'H_diversity': H_div,
        'H_flexibility': H_flex,
        'H_combinability': H_comb,
        'H_in_degree': H_in,
        'H_out_degree': H_out,
        'total_complexity': H_div + H_flex + H_comb,
    }


def calculate_node_complexity(G, node, payload):
    """
    Calculate complexity for a single node.
    
    Parameters:
    -----------
    G : NetworkX graph
        The network graph
    node : str
        Node name
    payload : dict
        Design payload
    
    Returns:
    --------
    dict
        Node complexity metrics
    """
    # Get node's neighbors
    neighbors = list(G.neighbors(node)) + list(G.predecessors(node))
    
    if not neighbors:
        return {
            'node': node,
            'degree': G.degree(node),
            'in_degree': G.in_degree(node),
            'out_degree': G.out_degree(node),
            'neighbor_diversity': 0.0,
            'connection_diversity': 0.0,
            'total_complexity': 0.0,
        }
    
    # Neighbor type diversity
    neighbor_types = [G.nodes[n].get('component_type', 'Unknown') for n in neighbors]
    neighbor_counts = Counter(neighbor_types)
    neighbor_probs = np.array([count / len(neighbors) for count in neighbor_counts.values()])
    H_neighbor = shannon_entropy(neighbor_probs)
    
    # Connection diversity for this node
    node_conn_types = []
    for edge in G.edges(data=True):
        u, v, attrs = edge
        if u == node:
            node_conn_types.append(attrs.get('from_conn', 'Unknown'))
        if v == node:
            node_conn_types.append(attrs.get('to_conn', 'Unknown'))
    
    if node_conn_types:
        conn_counts = Counter(node_conn_types)
        conn_probs = np.array([count / len(node_conn_types) for count in conn_counts.values()])
        H_conn = shannon_entropy(conn_probs)
    else:
        H_conn = 0.0
    
    total_complexity = H_neighbor + H_conn
    
    return {
        'node': node,
        'component_type': G.nodes[node].get('component_type', 'Unknown'),
        'degree': G.degree(node),
        'in_degree': G.in_degree(node),
        'out_degree': G.out_degree(node),
        'neighbor_diversity': H_neighbor,
        'connection_diversity': H_conn,
        'total_complexity': total_complexity,
    }


def calculate_all_node_complexities(G, payload):
    """
    Calculate complexity for all nodes in a graph.
    
    Parameters:
    -----------
    G : NetworkX graph
        The network graph
    payload : dict
        Design payload
    
    Returns:
    --------
    dict
        Dictionary mapping node names to complexity metrics
    """
    node_complexities = {}
    for node in G.nodes():
        node_complexities[node] = calculate_node_complexity(G, node, payload)
    return node_complexities


def analyze_design_complexity(all_designs_data, verbose=True):
    """
    Analyze complexity for all designs.
    
    Parameters:
    -----------
    all_designs_data : dict
        All design data
    verbose : bool
        Print progress
    
    Returns:
    --------
    dict
        Complexity analysis results
    """
    if verbose:
        print("\n" + "=" * 80)
        print("NODE COMPLEXITY ANALYSIS")
        print("=" * 80)
        print("Reference: Rebout et.al and De Wecl - Structural Complexity Analysis")
        print("=" * 80)
    
    results = {}
    
    for design_name, data in all_designs_data.items():
        G = data['G']
        payload = data['payload']
        
        # System-level complexity
        system_entropies = calculate_system_entropies(G, payload)
        
        # Node-level complexity
        node_complexities = calculate_all_node_complexities(G, payload)
        
        results[design_name] = {
            'system_entropies': system_entropies,
            'node_complexities': node_complexities,
        }
        
        if verbose:
            print(f"\n✓ {design_name}:")
            print(f"   System Complexity: {system_entropies['total_complexity']:.3f}")
            print(f"   Diversity:   {system_entropies['H_diversity']:.3f}")
            print(f"   Flexibility: {system_entropies['H_flexibility']:.3f}")
            print(f"   Combinability: {system_entropies['H_combinability']:.3f}")
    
    if verbose:
        print(f"\n✓ Complexity analysis completed for {len(results)} designs")
    
    return results


def get_complexity_summary(complexity_results):
    """
    Get summary statistics of complexity analysis.
    
    Parameters:
    -----------
    complexity_results : dict
        Complexity analysis results
    
    Returns:
    --------
    dict
        Summary statistics
    """
    total_complexities = []
    diversities = []
    flexibilities = []
    combinabilities = []
    
    for design_name, data in complexity_results.items():
        sys_ent = data['system_entropies']
        total_complexities.append(sys_ent['total_complexity'])
        diversities.append(sys_ent['H_diversity'])
        flexibilities.append(sys_ent['H_flexibility'])
        combinabilities.append(sys_ent['H_combinability'])
    
    return {
        'total_complexity': {
            'mean': np.mean(total_complexities),
            'std': np.std(total_complexities),
            'min': np.min(total_complexities),
            'max': np.max(total_complexities),
        },
        'diversity': {
            'mean': np.mean(diversities),
            'std': np.std(diversities),
        },
        'flexibility': {
            'mean': np.mean(flexibilities),
            'std': np.std(flexibilities),
        },
        'combinability': {
            'mean': np.mean(combinabilities),
            'std': np.std(combinabilities),
        },
    }


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    from .data_loader import load_all_designs
    
    # Test complexity analysis
    design_dirs = get_sorted_designs(DATA_ROOT)
    all_designs_data = load_all_designs(design_dirs, verbose=False)
    complexity_results = analyze_design_complexity(all_designs_data)
    
    summary = get_complexity_summary(complexity_results)
    print("\nComplexity Summary:")
    print(f"Total Complexity: {summary['total_complexity']['mean']:.3f} ± {summary['total_complexity']['std']:.3f}")
