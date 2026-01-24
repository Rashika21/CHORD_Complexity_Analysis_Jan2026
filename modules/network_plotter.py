"""
Network Plotter
===============
Visualization of UAV network graphs in 2D and 3D.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import numpy as np

from .config import CONFIG, COLOR_MAP
from .plot_utils import save_and_show, create_legend
from .setup import get_design_number


def plot_network_3d(G, pos_3d, title="Network Graph", ax=None, show_legend=True, save=False):
    """
    Plot network graph in 3D.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    pos_3d : dict
        Dictionary mapping nodes to (x, y, z) positions
    title : str
        Plot title
    ax : matplotlib 3D axes, optional
        Axes to plot on
    show_legend : bool
        Whether to show legend
    save : bool
        Whether to save plot
    
    Returns:
    --------
    ax
        The axes object
    """
    if ax is None:
        fig = plt.figure(figsize=CONFIG['plotting']['figsize_3d'])
        ax = fig.add_subplot(111, projection='3d')
    
    # Prepare node positions
    xs = [pos_3d[node][0] for node in G.nodes()]
    ys = [pos_3d[node][1] for node in G.nodes()]
    zs = [pos_3d[node][2] for node in G.nodes()]
    
    # Get node colors based on component type
    node_colors = [
        COLOR_MAP.get(G.nodes[node].get('component_type', 'Default'), COLOR_MAP['Default'])
        for node in G.nodes()
    ]
    
    # Draw edges
    for edge in G.edges():
        u, v = edge
        if u in pos_3d and v in pos_3d:
            xs_edge = [pos_3d[u][0], pos_3d[v][0]]
            ys_edge = [pos_3d[u][1], pos_3d[v][1]]
            zs_edge = [pos_3d[u][2], pos_3d[v][2]]
            ax.plot(xs_edge, ys_edge, zs_edge, 
                   c='gray', alpha=0.4, linewidth=0.8, zorder=1)
    
    # Draw nodes
    ax.scatter(xs, ys, zs, c=node_colors, s=100, alpha=0.9, 
              edgecolors='black', linewidths=0.5, zorder=2)
    
    # Set labels
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('X', fontsize=10)
    ax.set_ylabel('Y', fontsize=10)
    ax.set_zlabel('Z', fontsize=10)
    
    # Add legend
    if show_legend:
        create_legend(ax, G, COLOR_MAP, loc='upper left', fontsize=8)
    
    if save:
        save_and_show(ax.figure, title.replace(' ', '_'))
    
    return ax


def plot_all_networks_3d(all_designs_data, all_positions_3d, n_cols=5, save=True, complexity_results=None):
    """
    Plot 3D network graphs for all designs in a grid (3 rows x 5 columns for 15 designs).
    
    Parameters:
    -----------
    all_designs_data : dict
        All design data
    all_positions_3d : dict
        All 3D positions
    n_cols : int
        Number of columns in grid (default: 5 for 3x5 layout)
    save : bool
        Whether to save plot
    complexity_results : dict, optional
        Complexity analysis results to determine complexity level
    
    Returns:
    --------
    fig
        The figure object
    """
    print("\n" + "=" * 80)
    print("PLOTTING 3D NETWORK GRAPHS FOR ALL DESIGNS")
    print("=" * 80)
    
    sorted_designs = sorted(all_designs_data.keys(), key=get_design_number)
    n_designs = len(sorted_designs)
    n_rows = 3  # Fixed 3 rows for 15 designs
    n_cols = 5  # Fixed 5 columns for 15 designs
    
    # Determine complexity levels for each design
    complexity_levels = {}
    
    # Special assignments based on design selector (from PDF)
    complexity_levels['design_1'] = "Least Complexity"
    complexity_levels['design_14'] = "Medium Complexity"
    complexity_levels['design_5'] = "Highest Complexity"
    complexity_levels['design_12'] = "Non-Classical"
    
    if complexity_results:
        # Get total complexities
        total_complexities = {
            name: complexity_results[name]['system_entropies']['total_complexity']
            for name in sorted_designs if name in complexity_results
        }
        if total_complexities:
            sorted_by_complexity = sorted(total_complexities.items(), key=lambda x: x[1])
            n = len(sorted_by_complexity)
            low_threshold = sorted_by_complexity[n//3][1] if n >= 3 else sorted_by_complexity[0][1]
            high_threshold = sorted_by_complexity[2*n//3][1] if n >= 3 else sorted_by_complexity[-1][1]
            
            for name, comp in total_complexities.items():
                if name not in complexity_levels:  # Don't override special assignments
                    if comp <= low_threshold:
                        complexity_levels[name] = "Low Complexity"
                    elif comp >= high_threshold:
                        complexity_levels[name] = "High Complexity"
                    else:
                        complexity_levels[name] = "Medium Complexity"
    else:
        # If no complexity results, use node count as proxy
        node_counts = {name: all_designs_data[name]['num_nodes'] for name in sorted_designs}
        sorted_by_nodes = sorted(node_counts.items(), key=lambda x: x[1])
        n = len(sorted_by_nodes)
        low_threshold = sorted_by_nodes[n//3][1] if n >= 3 else sorted_by_nodes[0][1]
        high_threshold = sorted_by_nodes[2*n//3][1] if n >= 3 else sorted_by_nodes[-1][1]
        
        for name, node_count in node_counts.items():
            if name not in complexity_levels:  # Don't override special assignments
                if node_count <= low_threshold:
                    complexity_levels[name] = "Low Complexity"
                elif node_count >= high_threshold:
                    complexity_levels[name] = "High Complexity"
                else:
                    complexity_levels[name] = "Medium Complexity"
    
    fig = plt.figure(figsize=(20, 12))  # Larger figure for 3x5 grid
    
    for idx, design_name in enumerate(sorted_designs):
        data = all_designs_data[design_name]
        pos_3d = all_positions_3d[design_name]
        
        ax = fig.add_subplot(n_rows, n_cols, idx + 1, projection='3d')
        
        # Get complexity level
        comp_level = complexity_levels.get(design_name, "Medium Complexity")
        num_nodes = data['num_nodes']
        num_edges = data['num_edges']
        
        # Create subtitle with complexity level, nodes, and edges
        subtitle = f"{comp_level}\n{num_nodes} nodes, {num_edges} edges"
        
        plot_network_3d(
            data['G'], 
            pos_3d, 
            title=f"Design {get_design_number(design_name)}\n{subtitle}",
            ax=ax,
            show_legend=False,  # No legend to avoid overlap
            save=False
        )
        
        # Adjust title position and size to avoid overlap
        ax.title.set_position([0.5, 1.08])  # Move title up
        ax.title.set_fontsize(8)
        ax.title.set_fontweight('bold')
        
        # Remove axis labels to reduce clutter
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_zlabel('')
        ax.tick_params(labelsize=5, pad=0)
        
        # Adjust view angle for better visibility
        ax.view_init(elev=20, azim=45)
    
    plt.suptitle(f'3D Network Graphs - All {n_designs} Designs',
                 fontsize=18, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.98], pad=2.0)  # Extra padding to avoid overlap
    
    if save:
        save_and_show(fig, '3D_Network_Graphs_All')
    
    print(f"✓ 3D network plots created for {n_designs} designs")
    
    return fig


def plot_selected_networks_3d(all_designs_data, all_positions_3d, design_indices, 
                               titles=None, save=True):
    """
    Plot 3D networks for selected designs.
    
    Parameters:
    -----------
    all_designs_data : dict
        All design data
    all_positions_3d : dict
        All 3D positions
    design_indices : list
        Indices of designs to plot
    titles : list, optional
        Custom titles
    save : bool
        Whether to save
    
    Returns:
    --------
    fig
        The figure object
    """
    n_designs = len(design_indices)
    n_cols = min(n_designs, 2)
    n_rows = (n_designs + n_cols - 1) // n_cols
    
    fig = plt.figure(figsize=(12 * n_cols, 10 * n_rows))
    
    design_names = sorted(all_designs_data.keys(), key=get_design_number)
    
    for i, idx in enumerate(design_indices):
        design_name = design_names[idx]
        data = all_designs_data[design_name]
        pos_3d = all_positions_3d[design_name]
        
        ax = fig.add_subplot(n_rows, n_cols, i + 1, projection='3d')
        
        title = titles[i] if titles and i < len(titles) else design_name
        plot_network_3d(
            data['G'],
            pos_3d,
            title=title,
            ax=ax,
            show_legend=True,
            save=False
        )
    
    plt.suptitle('Selected Network Graphs - 3D View',
                 fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    if save:
        save_and_show(fig, 'Selected_Networks_3D')
    
    return fig


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    from .data_loader import load_all_designs
    from .geometry_parser import parse_all_geometries
    from .position_calculator import calculate_all_positions
    
    # Test network plotting
    design_dirs = get_sorted_designs(DATA_ROOT)
    all_designs_data = load_all_designs(design_dirs, verbose=False)
    designs_geometry = parse_all_geometries(all_designs_data, verbose=False)
    all_positions_3d = calculate_all_positions(all_designs_data, designs_geometry, verbose=False)
    
    # Plot first design
    first_design = sorted(all_designs_data.keys(), key=get_design_number)[0]
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    plot_network_3d(
        all_designs_data[first_design]['G'],
        all_positions_3d[first_design],
        title=first_design,
        ax=ax,
        show_legend=True,
        save=True
    )
    print("✓ Network plotting test completed")
