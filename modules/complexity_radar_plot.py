"""
Complexity Radar Plot
=====================
Create radar/spider plots for visualizing multi-dimensional complexity metrics.
Shows Flexibility, Combinability, and Diversity for comparison across designs.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple
from .config import CONFIG
from .plot_utils import save_and_show
from .setup import get_design_number


def create_radar_plot(ax, design_name: str, flex_val: float, comb_val: float, 
                     div_val: float, color: str, alpha: float = 0.7) -> plt.Axes:
    """
    Create a radar plot for a single design.
    
    Parameters:
    -----------
    ax : matplotlib polar axis
        The polar axis to plot on
    design_name : str
        Name of the design
    flex_val, comb_val, div_val : float
        Values for flexibility, combinability, diversity
    color : str or tuple
        Color for the plot
    alpha : float
        Transparency (default: 0.7)
    
    Returns:
    --------
    matplotlib.axes.Axes
        The polar axis with plot
    """
    # Categories for radar plot
    categories = ['Flexibility', 'Combinability', 'Diversity']
    N = len(categories)
    
    # Compute angle for each category
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    # Values for this design
    values = [flex_val, comb_val, div_val]
    values += values[:1]  # Complete the circle
    
    # Plot
    ax.plot(angles, values, 'o-', linewidth=2, label=design_name, 
            color=color, alpha=alpha)
    ax.fill(angles, values, alpha=0.15, color=color)
    
    # Add labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
    
    return ax


def prepare_radar_data(complexity_results: Dict, component_type: str = 'Motor') -> Dict:
    """
    Prepare radar plot data from complexity analysis results.
    
    Parameters:
    -----------
    complexity_results : dict
        Results from analyze_design_complexity()
    component_type : str
        Component type to analyze (default: 'Motor')
    
    Returns:
    --------
    dict
        Dictionary mapping design names to radar plot data
    """
    radar_data = {}
    
    for design_name, data in complexity_results.items():
        # Get node complexities
        node_complexities = data.get('node_complexities', {})
        
        # Filter by component type
        component_nodes = {
            node: metrics for node, metrics in node_complexities.items()
            if metrics.get('component_type') == component_type
        }
        
        if component_nodes:
            # Calculate averages for this component type
            flexibilities = [m.get('connection_diversity', 0.0) 
                           for m in component_nodes.values()]
            combinabilities = [m.get('neighbor_diversity', 0.0) 
                             for m in component_nodes.values()]
            diversities = [m.get('total_complexity', 0.0) / 3.0  # Rough estimate
                          for m in component_nodes.values()]
            
            radar_data[design_name] = {
                'flexibility': np.mean(flexibilities) if flexibilities else 0.0,
                'combinability': np.mean(combinabilities) if combinabilities else 0.0,
                'diversity': np.mean(diversities) if diversities else 0.0,
                'count': len(component_nodes)
            }
        else:
            radar_data[design_name] = {
                'flexibility': 0.0,
                'combinability': 0.0,
                'diversity': 0.0,
                'count': 0
            }
    
    return radar_data


def plot_radar_overview(radar_data: Dict, sorted_design_names: List[str],
                       title: str = "Complexity Radar Plot: All Designs",
                       save: bool = True) -> plt.Figure:
    """
    Create a single radar plot with all designs (overview).
    
    Parameters:
    -----------
    radar_data : dict
        Radar plot data from prepare_radar_data()
    sorted_design_names : list
        List of design names in sorted order
    title : str
        Plot title
    save : bool
        Whether to save the plot (default: True)
    
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object
    """
    # Find global min and max for consistent axis scaling
    all_flex = [radar_data[d]['flexibility'] for d in sorted_design_names if d in radar_data]
    all_comb = [radar_data[d]['combinability'] for d in sorted_design_names if d in radar_data]
    all_div = [radar_data[d]['diversity'] for d in sorted_design_names if d in radar_data]
    
    global_min = min([min(all_flex), min(all_comb), min(all_div)])
    global_max = max([max(all_flex), max(all_comb), max(all_div)])
    axis_min = max(0, global_min - 0.5)
    axis_max = global_max + 0.5
    
    # Create color map for designs
    design_colors = plt.cm.tab20(np.linspace(0, 1, len(sorted_design_names)))
    design_color_map = {design_name: design_colors[i] 
                       for i, design_name in enumerate(sorted_design_names)}
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))
    
    categories = ['Flexibility', 'Combinability', 'Diversity']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Plot each design
    for design_name in sorted_design_names:
        if design_name not in radar_data or radar_data[design_name]['count'] == 0:
            continue
        
        design_num = get_design_number(design_name)
        flex_val = radar_data[design_name]['flexibility']
        comb_val = radar_data[design_name]['combinability']
        div_val = radar_data[design_name]['diversity']
        color = design_color_map[design_name]
        
        values = [flex_val, comb_val, div_val]
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=1.5, label=f'D{design_num}', 
               color=color, alpha=0.6, markersize=4)
        ax.fill(angles, values, alpha=0.05, color=color)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
    ax.set_ylim(axis_min, axis_max)
    ax.set_yticks(np.linspace(axis_min, axis_max, 5))
    ax.set_yticklabels([f'{val:.2f}' for val in np.linspace(axis_min, axis_max, 5)], 
                       fontsize=9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=8, ncol=2)
    
    plt.tight_layout()
    
    if save:
        filename = title.replace('\n', '_').replace(' ', '_').replace(':', '')
        save_and_show(fig, filename, show=True)
    
    return fig


def plot_radar_grid(radar_data: Dict, sorted_design_names: List[str],
                   title: str = "Complexity Radar Plots: Individual Designs",
                   rows: int = 3, cols: int = 5, save: bool = True) -> plt.Figure:
    """
    Create a grid of individual radar plots (one per design).
    
    Parameters:
    -----------
    radar_data : dict
        Radar plot data from prepare_radar_data()
    sorted_design_names : list
        List of design names in sorted order
    title : str
        Plot title
    rows : int
        Number of rows in grid (default: 3)
    cols : int
        Number of columns in grid (default: 5)
    save : bool
        Whether to save the plot (default: True)
    
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object
    """
    # Find global min and max for consistent axis scaling
    all_flex = [radar_data[d]['flexibility'] for d in sorted_design_names if d in radar_data]
    all_comb = [radar_data[d]['combinability'] for d in sorted_design_names if d in radar_data]
    all_div = [radar_data[d]['diversity'] for d in sorted_design_names if d in radar_data]
    
    global_min = min([min(all_flex), min(all_comb), min(all_div)])
    global_max = max([max(all_flex), max(all_comb), max(all_div)])
    axis_min = max(0, global_min - 0.5)
    axis_max = global_max + 0.5
    
    # Create color map for designs
    design_colors = plt.cm.tab20(np.linspace(0, 1, len(sorted_design_names)))
    design_color_map = {design_name: design_colors[i] 
                       for i, design_name in enumerate(sorted_design_names)}
    
    # Create figure with grid
    fig, axes = plt.subplots(rows, cols, figsize=(22, 14), 
                            subplot_kw=dict(projection='polar'))
    axes = axes.flatten()
    
    categories = ['Flexibility', 'Combinability', 'Diversity']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Plot each design
    for idx, design_name in enumerate(sorted_design_names):
        if idx >= len(axes):
            break
        
        ax = axes[idx]
        
        if design_name not in radar_data or radar_data[design_name]['count'] == 0:
            ax.axis('off')
            continue
        
        design_num = get_design_number(design_name)
        flex_val = radar_data[design_name]['flexibility']
        comb_val = radar_data[design_name]['combinability']
        div_val = radar_data[design_name]['diversity']
        color = design_color_map[design_name]
        
        values = [flex_val, comb_val, div_val]
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2.5, color=color, alpha=0.8, markersize=6)
        ax.fill(angles, values, alpha=0.25, color=color)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=9, fontweight='bold')
        ax.set_ylim(axis_min, axis_max)
        ax.set_yticks(np.linspace(axis_min, axis_max, 4))
        ax.set_yticklabels([f'{val:.2f}' for val in np.linspace(axis_min, axis_max, 4)], 
                          fontsize=7)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_title(f'Design {design_num}\nFlex:{flex_val:.2f} Comb:{comb_val:.2f} Div:{div_val:.2f}', 
                    fontsize=10, fontweight='bold', pad=10)
    
    # Hide any extra subplots
    for extra_ax in axes[len(sorted_design_names):]:
        extra_ax.axis('off')
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if save:
        filename = title.replace('\n', '_').replace(' ', '_').replace(':', '')
        save_and_show(fig, filename, show=True)
    
    return fig


def plot_radar_by_complexity(radar_data: Dict, sorted_design_names: List[str],
                            title: str = "Complexity Radar Plots: Grouped by Complexity Level",
                            save: bool = True) -> plt.Figure:
    """
    Create grouped radar plots by complexity level.
    
    Parameters:
    -----------
    radar_data : dict
        Radar plot data from prepare_radar_data()
    sorted_design_names : list
        List of design names in sorted order
    title : str
        Plot title
    save : bool
        Whether to save the plot (default: True)
    
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object
    """
    # Calculate total complexity for each design
    design_total_complexity = {}
    for design_name in sorted_design_names:
        if design_name in radar_data:
            total = (radar_data[design_name]['flexibility'] + 
                    radar_data[design_name]['combinability'] + 
                    radar_data[design_name]['diversity'])
            design_total_complexity[design_name] = total
    
    # Sort by total complexity
    sorted_by_complexity = sorted(design_total_complexity.items(), key=lambda x: x[1])
    n_designs = len(sorted_by_complexity)
    
    low_complexity = [d[0] for d in sorted_by_complexity[:n_designs//3]]
    medium_complexity = [d[0] for d in sorted_by_complexity[n_designs//3:2*n_designs//3]]
    high_complexity = [d[0] for d in sorted_by_complexity[2*n_designs//3:]]
    
    # Find global min and max for consistent axis scaling
    all_flex = [radar_data[d]['flexibility'] for d in sorted_design_names if d in radar_data]
    all_comb = [radar_data[d]['combinability'] for d in sorted_design_names if d in radar_data]
    all_div = [radar_data[d]['diversity'] for d in sorted_design_names if d in radar_data]
    
    global_min = min([min(all_flex), min(all_comb), min(all_div)])
    global_max = max([max(all_flex), max(all_comb), max(all_div)])
    axis_min = max(0, global_min - 0.5)
    axis_max = global_max + 0.5
    
    # Create figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw=dict(projection='polar'))
    
    categories = ['Flexibility', 'Combinability', 'Diversity']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    groups = [
        (low_complexity, 'Low Complexity Designs', axes[0], '#2E86AB'),
        (medium_complexity, 'Medium Complexity Designs', axes[1], '#A23B72'),
        (high_complexity, 'High Complexity Designs', axes[2], '#F18F01')
    ]
    
    for group_designs, group_title, ax, base_color in groups:
        for design_name in group_designs:
            if design_name not in radar_data or radar_data[design_name]['count'] == 0:
                continue
            
            design_num = get_design_number(design_name)
            flex_val = radar_data[design_name]['flexibility']
            comb_val = radar_data[design_name]['combinability']
            div_val = radar_data[design_name]['diversity']
            
            values = [flex_val, comb_val, div_val]
            values += values[:1]
            
            # Use slightly different shades of base color
            color_idx = group_designs.index(design_name)
            if base_color == '#2E86AB':
                color = plt.cm.Blues(0.3 + 0.5 * color_idx / len(group_designs))
            elif base_color == '#A23B72':
                color = plt.cm.Purples(0.3 + 0.5 * color_idx / len(group_designs))
            else:
                color = plt.cm.Oranges(0.3 + 0.5 * color_idx / len(group_designs))
            
            ax.plot(angles, values, 'o-', linewidth=2, label=f'D{design_num}', 
                   color=color, alpha=0.7, markersize=5)
            ax.fill(angles, values, alpha=0.1, color=color)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
        ax.set_ylim(axis_min, axis_max)
        ax.set_yticks(np.linspace(axis_min, axis_max, 4))
        ax.set_yticklabels([f'{val:.2f}' for val in np.linspace(axis_min, axis_max, 4)], 
                          fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_title(group_title, fontsize=12, fontweight='bold', pad=15)
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=8)
    
    plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if save:
        filename = title.replace('\n', '_').replace(' ', '_').replace(':', '')
        save_and_show(fig, filename, show=True)
    
    return fig


def create_all_radar_plots(complexity_results: Dict, sorted_design_names: List[str],
                          component_type: str = 'Motor', save: bool = True,
                          verbose: bool = True) -> Dict[str, plt.Figure]:
    """
    Create all radar plot variants.
    
    Parameters:
    -----------
    complexity_results : dict
        Results from analyze_design_complexity()
    sorted_design_names : list
        List of design names in sorted order
    component_type : str
        Component type to analyze (default: 'Motor')
    save : bool
        Whether to save plots (default: True)
    verbose : bool
        Print progress (default: True)
    
    Returns:
    --------
    dict
        Dictionary of figure objects for each plot type
    """
    if verbose:
        print("\n" + "=" * 80)
        print(f"CREATING RADAR PLOTS: {component_type.upper()} COMPLEXITY")
        print("=" * 80)
    
    # Prepare data
    radar_data = prepare_radar_data(complexity_results, component_type)
    
    if verbose:
        print(f"\n✓ Prepared radar data for {len(radar_data)} designs")
    
    # Create plots
    figures = {}
    
    if verbose:
        print("\n📊 Creating overview radar plot...")
    figures['overview'] = plot_radar_overview(
        radar_data, sorted_design_names,
        title=f"{component_type} Complexity Radar Plot: All Designs\n(Flexibility, Combinability, Diversity)",
        save=save
    )
    
    if verbose:
        print("✓ Overview radar plot created")
        print("\n📊 Creating grid of individual radar plots...")
    figures['grid'] = plot_radar_grid(
        radar_data, sorted_design_names,
        title=f"{component_type} Complexity Radar Plots: Individual Designs\n(Flexibility, Combinability, Diversity)",
        save=save
    )
    
    if verbose:
        print("✓ Grid of individual radar plots created")
        print("\n📊 Creating grouped radar plots by complexity level...")
    figures['grouped'] = plot_radar_by_complexity(
        radar_data, sorted_design_names,
        title=f"{component_type} Complexity Radar Plots: Grouped by Complexity Level",
        save=save
    )
    
    if verbose:
        print("✓ Grouped radar plots created")
        print("\n" + "=" * 80)
        print("✓ RADAR PLOTS COMPLETE")
        print("=" * 80)
    
    return figures


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    from .data_loader import load_all_designs
    from .complexity_analyzer import analyze_design_complexity
    
    # Test radar plots
    design_dirs = get_sorted_designs(DATA_ROOT)
    all_designs_data = load_all_designs(design_dirs, verbose=False)
    complexity_results = analyze_design_complexity(all_designs_data, verbose=False)
    sorted_design_names = sorted(all_designs_data.keys(), key=get_design_number)
    
    figures = create_all_radar_plots(complexity_results, sorted_design_names, 
                                     component_type='Motor', verbose=True)
