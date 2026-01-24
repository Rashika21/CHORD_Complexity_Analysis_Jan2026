"""
Complexity Box and Violin Plot
===============================
Create box plots and violin plots for visualizing complexity distributions.
Box plots show quartiles, median, and outliers.
Violin plots show distribution shape with box plot overlay.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from typing import Dict, List, Optional, Tuple
from .config import CONFIG
from .plot_utils import save_and_show


def prepare_box_plot_data(complexity_results: Dict, selected_designs: Optional[List] = None) -> Tuple[List, List, Dict]:
    """
    Prepare data for box plot from complexity analysis results.
    
    Parameters:
    -----------
    complexity_results : dict
        Results from analyze_design_complexity()
    selected_designs : list, optional
        List of (label, stats) tuples for selected designs.
        If None, uses all designs.
    
    Returns:
    --------
    tuple
        (box_plot_data, box_plot_labels, box_plot_stats)
    """
    box_plot_data = []
    box_plot_labels = []
    box_plot_stats = {}
    
    if selected_designs is None:
        # Use all designs
        selected_designs = [
            (design_name, {'design_name': design_name, 'node_complexity': data.get('node_complexities', {})})
            for design_name, data in complexity_results.items()
        ]
    
    for label, stats in selected_designs:
        design_name = stats.get('design_name', label)
        node_comp = stats.get('node_complexity', {})
        
        if node_comp:
            # Extract total complexity values
            complexities = [nc.get('total_complexity', 0.0) for nc in node_comp.values()]
            
            if complexities:
                box_plot_data.append(complexities)
                box_plot_labels.append(f"{label}\n({design_name})")
                
                # Calculate statistics
                q1 = np.percentile(complexities, 25)
                q3 = np.percentile(complexities, 75)
                iqr = q3 - q1
                
                box_plot_stats[label] = {
                    'mean': np.mean(complexities),
                    'median': np.median(complexities),
                    'std': np.std(complexities),
                    'min': np.min(complexities),
                    'max': np.max(complexities),
                    'q1': q1,
                    'q3': q3,
                    'iqr': iqr,
                    'design_name': design_name,
                    'data': complexities,
                    'num_nodes': len(complexities)
                }
    
    return box_plot_data, box_plot_labels, box_plot_stats


def plot_box_plot(box_plot_data: List, box_plot_labels: List, 
                 box_plot_stats: Dict, title: str = "Node Complexity Distribution: Box Plot",
                 save: bool = True, figsize: Tuple[int, int] = (16, 10)) -> plt.Figure:
    """
    Create a box plot showing complexity distributions.
    
    Parameters:
    -----------
    box_plot_data : list
        List of lists containing complexity values for each design
    box_plot_labels : list
        List of labels for each design
    box_plot_stats : dict
        Dictionary of statistics for each design
    title : str
        Plot title
    save : bool
        Whether to save the plot (default: True)
    figsize : tuple
        Figure size (default: (16, 10))
    
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create box plot
    bp = ax.boxplot(box_plot_data, labels=box_plot_labels, patch_artist=True,
                   showmeans=True, meanline=True,
                   boxprops=dict(facecolor='lightblue', alpha=0.7, linewidth=2.5, edgecolor='navy'),
                   medianprops=dict(color='red', linewidth=3, linestyle='--', label='Median'),
                   meanprops=dict(color='green', linewidth=3, linestyle='-', label='Mean'),
                   whiskerprops=dict(linewidth=2.5, color='black'),
                   capprops=dict(linewidth=2.5, color='black'),
                   flierprops=dict(marker='o', markersize=8, alpha=0.7,
                                 markerfacecolor='red', markeredgecolor='darkred',
                                 markeredgewidth=1.5, label='Outliers'))
    
    # Customize colors for each box
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#C7CEEA']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
        patch.set_edgecolor('navy')
        patch.set_linewidth(2.5)
    
    # Add value annotations
    for i, (label, stats_data) in enumerate(box_plot_stats.items()):
        x_pos = i + 1
        mean_val = stats_data['mean']
        std_val = stats_data['std']
        min_val = stats_data['min']
        max_val = stats_data['max']
        
        # Add key complexity values
        ax.text(x_pos, mean_val + 0.5, f'Mean={mean_val:.2f}', ha='center', va='bottom',
               fontsize=10, fontweight='bold', color='green',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.8))
        ax.text(x_pos, min_val - 0.5, f'Min={min_val:.2f}', ha='center', va='top',
               fontsize=9, fontweight='bold', color='darkblue',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcyan', alpha=0.8))
        ax.text(x_pos, max_val + 0.5, f'Max={max_val:.2f}', ha='center', va='bottom',
               fontsize=9, fontweight='bold', color='darkblue',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcyan', alpha=0.8))
        ax.text(x_pos, mean_val - 1.2, f'SD={std_val:.2f}', ha='center', va='top',
               fontsize=10, fontweight='bold', color='orange',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='wheat', alpha=0.8))
    
    ax.grid(True, alpha=0.3, linestyle='--', axis='y', linewidth=1)
    ax.set_ylabel('Node Complexity Value', fontsize=13, fontweight='bold')
    ax.set_xlabel('Design Category', fontsize=13, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Create legend
    legend_elements = [
        Patch(facecolor='lightblue', alpha=0.7, edgecolor='navy', linewidth=2,
             label='Box (IQR): Middle 50% of data\n(Q1 to Q3)'),
        plt.Line2D([0], [0], color='red', linewidth=3, linestyle='--',
                  label='Median: Middle value (50th percentile)'),
        plt.Line2D([0], [0], color='green', linewidth=3, linestyle='-',
                  label='Mean: Average value'),
        plt.Line2D([0], [0], color='black', linewidth=2.5,
                  label='Whiskers: Data range (1.5×IQR)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red',
                  markersize=10, markeredgecolor='darkred', markeredgewidth=1.5,
                  linestyle='None', label='Outliers: Unusual values (>1.5×IQR)')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10,
             framealpha=0.95, fancybox=True, shadow=True)
    
    plt.tight_layout()
    
    if save:
        filename = title.replace('\n', '_').replace(' ', '_').replace(':', '')
        save_and_show(fig, filename, show=True)
    
    return fig


def plot_violin_with_box(box_plot_data: List, box_plot_labels: List,
                        box_plot_stats: Dict, title: str = "Violin Plot: Node Complexity Distribution",
                        save: bool = True, figsize: Tuple[int, int] = (14, 10)) -> plt.Figure:
    """
    Create a violin plot with box plot overlay.
    
    Parameters:
    -----------
    box_plot_data : list
        List of lists containing complexity values for each design
    box_plot_labels : list
        List of labels for each design
    box_plot_stats : dict
        Dictionary of statistics for each design
    title : str
        Plot title
    save : bool
        Whether to save the plot (default: True)
    figsize : tuple
        Figure size (default: (14, 10))
    
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Calculate y-axis limits with padding
    all_min_vals = [stats_data['min'] for stats_data in box_plot_stats.values()]
    all_max_vals = [stats_data['max'] for stats_data in box_plot_stats.values()]
    global_min = min(all_min_vals)
    global_max = max(all_max_vals)
    global_range = global_max - global_min
    y_padding = global_range * 0.15
    y_min = global_min - y_padding - 1.0
    y_max = global_max + y_padding + 2.0
    
    # Create violin plot
    parts = ax.violinplot(box_plot_data,
                         positions=range(1, len(box_plot_data) + 1),
                         showmeans=True, showmedians=True,
                         widths=0.7, bw_method='scott')
    
    # Overlay box plot
    bp = ax.boxplot(box_plot_data, labels=box_plot_labels,
                   patch_artist=True, widths=0.25,
                   boxprops=dict(linewidth=2, edgecolor='black', facecolor='white', alpha=0.6),
                   medianprops=dict(color='red', linewidth=2.5, linestyle='--'),
                   meanprops=dict(color='green', linewidth=2.5, linestyle='-'),
                   whiskerprops=dict(linewidth=2, color='black'),
                   capprops=dict(linewidth=2, color='black'),
                   flierprops=dict(marker='o', markersize=6, alpha=0.6,
                                 markerfacecolor='red', markeredgecolor='darkred'))
    
    # Color violins
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#C7CEEA']
    for pc, color in zip(parts['bodies'], colors[:len(parts['bodies'])]):
        pc.set_facecolor(color)
        pc.set_alpha(0.65)
        pc.set_edgecolor('black')
        pc.set_linewidth(1.5)
    
    # Set y-axis limits
    ax.set_ylim(y_min, y_max)
    
    # Add value labels
    for i, (label, stats_data) in enumerate(box_plot_stats.items()):
        x_pos = i + 1
        mean_val = stats_data['mean']
        std_val = stats_data['std']
        min_val = stats_data['min']
        max_val = stats_data['max']
        
        data_range = max_val - min_val
        spacing_factor = max(0.8, data_range * 0.12)
        
        # Mean
        ax.text(x_pos, mean_val + spacing_factor * 0.6, f'Mean: {mean_val:.2f}',
               ha='center', va='bottom',
               fontsize=12, fontweight='bold', color='#2E7D32',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='#C8E6C9', alpha=0.9,
                        edgecolor='#2E7D32', linewidth=1.5))
        
        # Min
        min_label_y = max(min_val - spacing_factor * 0.5, y_min + 0.3)
        ax.text(x_pos - 0.15, min_label_y, f'Min: {min_val:.2f}',
               ha='right', va='top',
               fontsize=11, fontweight='bold', color='#1565C0',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#BBDEFB', alpha=0.9,
                        edgecolor='#1565C0', linewidth=1.5))
        
        # Max
        max_label_y = min(max_val + spacing_factor * 0.5, y_max - 0.3)
        ax.text(x_pos + 0.15, max_label_y, f'Max: {max_val:.2f}',
               ha='left', va='bottom',
               fontsize=11, fontweight='bold', color='#6A1B9A',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#E1BEE7', alpha=0.9,
                        edgecolor='#6A1B9A', linewidth=1.5))
        
        # Standard Deviation
        ax.text(x_pos, mean_val - spacing_factor * 0.7, f'SD: {std_val:.2f}',
               ha='center', va='top',
               fontsize=11, fontweight='bold', color='#E65100',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFE0B2', alpha=0.9,
                        edgecolor='#E65100', linewidth=1.5))
    
    ax.grid(True, alpha=0.3, linestyle='--', axis='y', linewidth=1.5)
    ax.set_ylabel('Node Complexity Value (Entropy-based)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Design Category', fontsize=14, fontweight='bold')
    ax.set_title(title, fontsize=15, fontweight='bold', pad=25)
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#2E7D32', lw=4, label='Mean (Average Complexity)'),
        Line2D([0], [0], color='#1565C0', lw=4, label='Min (Minimum Complexity)'),
        Line2D([0], [0], color='#6A1B9A', lw=4, label='Max (Maximum Complexity)'),
        Line2D([0], [0], color='#E65100', lw=4, label='SD (Standard Deviation)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
             framealpha=0.95, title='Complexity Metrics', title_fontsize=13,
             edgecolor='black', fancybox=True, shadow=True)
    
    plt.tight_layout()
    
    if save:
        filename = title.replace('\n', '_').replace(' ', '_').replace(':', '')
        save_and_show(fig, filename, show=True)
    
    return fig


def plot_combined_box_violin(box_plot_data: List, box_plot_labels: List,
                            box_plot_stats: Dict,
                            title: str = "Complexity Distribution Comparison",
                            save: bool = True, figsize: Tuple[int, int] = (20, 10)) -> plt.Figure:
    """
    Create side-by-side box plot and violin plot.
    
    Parameters:
    -----------
    box_plot_data : list
        List of lists containing complexity values for each design
    box_plot_labels : list
        List of labels for each design
    box_plot_stats : dict
        Dictionary of statistics for each design
    title : str
        Plot title
    save : bool
        Whether to save the plot (default: True)
    figsize : tuple
        Figure size (default: (20, 10))
    
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#C7CEEA']
    
    # Left plot: Box plot
    bp1 = ax1.boxplot(box_plot_data, labels=box_plot_labels,
                     patch_artist=True, showmeans=True, meanline=True,
                     boxprops=dict(facecolor='lightblue', alpha=0.7, linewidth=2.5, edgecolor='navy'),
                     medianprops=dict(color='red', linewidth=3, linestyle='--'),
                     meanprops=dict(color='green', linewidth=3, linestyle='-'),
                     whiskerprops=dict(linewidth=2.5, color='black'),
                     capprops=dict(linewidth=2.5, color='black'),
                     flierprops=dict(marker='o', markersize=10, alpha=0.8,
                                   markerfacecolor='red', markeredgecolor='darkred',
                                   markeredgewidth=2))
    
    for patch, color in zip(bp1['boxes'], colors[:len(bp1['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
        patch.set_edgecolor('navy')
        patch.set_linewidth(2.5)
    
    # Add annotations to box plot
    for i, (label, stats_data) in enumerate(box_plot_stats.items()):
        x_pos = i + 1
        mean_val = stats_data['mean']
        std_val = stats_data['std']
        min_val = stats_data['min']
        max_val = stats_data['max']
        
        ax1.text(x_pos, mean_val + 0.5, f'Mean={mean_val:.2f}', ha='center', va='bottom',
                fontsize=10, fontweight='bold', color='green',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.8))
        ax1.text(x_pos, min_val - 0.5, f'Min={min_val:.2f}', ha='center', va='top',
                fontsize=9, fontweight='bold', color='darkblue',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcyan', alpha=0.8))
        ax1.text(x_pos, max_val + 0.5, f'Max={max_val:.2f}', ha='center', va='bottom',
                fontsize=9, fontweight='bold', color='darkblue',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcyan', alpha=0.8))
        ax1.text(x_pos, mean_val - 1.2, f'SD={std_val:.2f}', ha='center', va='top',
                fontsize=10, fontweight='bold', color='orange',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='wheat', alpha=0.8))
    
    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax1.set_ylabel('Node Complexity Value', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Design Category', fontsize=13, fontweight='bold')
    ax1.set_title('Box Plot: Complexity Distribution\nValues Shown: Mean, Min, Max, Standard Deviation',
                 fontsize=14, fontweight='bold', pad=20)
    
    # Right plot: Violin plot with box overlay
    all_min_vals = [stats_data['min'] for stats_data in box_plot_stats.values()]
    all_max_vals = [stats_data['max'] for stats_data in box_plot_stats.values()]
    global_min = min(all_min_vals)
    global_max = max(all_max_vals)
    global_range = global_max - global_min
    y_padding = global_range * 0.15
    y_min = global_min - y_padding - 1.0
    y_max = global_max + y_padding + 2.0
    
    parts = ax2.violinplot(box_plot_data, positions=range(1, len(box_plot_data) + 1),
                          showmeans=True, showmedians=True, widths=0.7, bw_method='scott')
    
    bp2 = ax2.boxplot(box_plot_data, labels=box_plot_labels,
                     patch_artist=True, widths=0.3,
                     boxprops=dict(linewidth=2, edgecolor='black', facecolor='white', alpha=0.6),
                     medianprops=dict(color='red', linewidth=2.5, linestyle='--'),
                     meanprops=dict(color='green', linewidth=2.5, linestyle='-'),
                     whiskerprops=dict(linewidth=2, color='black'),
                     capprops=dict(linewidth=2, color='black'),
                     flierprops=dict(marker='o', markersize=6, alpha=0.6,
                                   markerfacecolor='red', markeredgecolor='darkred'))
    
    for pc, color in zip(parts['bodies'], colors[:len(parts['bodies'])]):
        pc.set_facecolor(color)
        pc.set_alpha(0.6)
    
    ax2.set_ylim(y_min, y_max)
    
    # Add annotations to violin plot
    for i, (label, stats_data) in enumerate(box_plot_stats.items()):
        x_pos = i + 1
        mean_val = stats_data['mean']
        std_val = stats_data['std']
        min_val = stats_data['min']
        max_val = stats_data['max']
        
        data_range = max_val - min_val
        spacing_factor = max(0.8, data_range * 0.15)
        
        ax2.text(x_pos, mean_val + spacing_factor * 0.6, f'Mean={mean_val:.2f}',
                ha='center', va='bottom',
                fontsize=10, fontweight='bold', color='green',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.8))
        ax2.text(x_pos, min_val - 0.8, f'Min={min_val:.2f}',
                ha='center', va='top',
                fontsize=9, fontweight='bold', color='darkblue',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcyan', alpha=0.8))
        ax2.text(x_pos, max_val + 0.8, f'Max={max_val:.2f}',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold', color='darkblue',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcyan', alpha=0.8))
        ax2.text(x_pos, mean_val - 1.2, f'SD={std_val:.2f}',
                ha='center', va='top',
                fontsize=10, fontweight='bold', color='orange',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='wheat', alpha=0.8))
    
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax2.set_ylabel('Node Complexity Value', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Design Category', fontsize=13, fontweight='bold')
    ax2.set_title('Violin Plot + Box Plot Overlay\nShows Full Distribution Shape (Mean, Min, Max, SD)',
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    if save:
        filename = title.replace('\n', '_').replace(' ', '_').replace(':', '')
        save_and_show(fig, filename, show=True)
    
    return fig


def create_all_box_violin_plots(complexity_results: Dict,
                               selected_designs: Optional[List] = None,
                               save: bool = True, verbose: bool = True) -> Dict[str, plt.Figure]:
    """
    Create all box and violin plot variants.
    
    Parameters:
    -----------
    complexity_results : dict
        Results from analyze_design_complexity()
    selected_designs : list, optional
        List of (label, stats) tuples for selected designs.
        If None, uses all designs.
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
        print("CREATING BOX AND VIOLIN PLOTS: COMPLEXITY DISTRIBUTION")
        print("=" * 80)
    
    # Prepare data
    box_plot_data, box_plot_labels, box_plot_stats = prepare_box_plot_data(
        complexity_results, selected_designs
    )
    
    if verbose:
        print(f"\n✓ Prepared box plot data for {len(box_plot_data)} designs")
    
    # Create plots
    figures = {}
    
    if verbose:
        print("\n📊 Creating box plot...")
    figures['box'] = plot_box_plot(
        box_plot_data, box_plot_labels, box_plot_stats,
        title="Node Complexity Distribution: Box Plot\n4 Selected Representative Designs with Statistical Details",
        save=save
    )
    
    if verbose:
        print("✓ Box plot created")
        print("\n📊 Creating violin plot with box overlay...")
    figures['violin'] = plot_violin_with_box(
        box_plot_data, box_plot_labels, box_plot_stats,
        title="Violin Plot: Node Complexity Distribution Analysis\n4 Selected Representative UAV Designs",
        save=save
    )
    
    if verbose:
        print("✓ Violin plot created")
        print("\n📊 Creating combined box and violin plot...")
    figures['combined'] = plot_combined_box_violin(
        box_plot_data, box_plot_labels, box_plot_stats,
        title="Block 11.6: Enhanced Complexity Visualization\nLeft: Box Plot with Value Labels | Right: Distribution Shape (Violin + Box)",
        save=save
    )
    
    if verbose:
        print("✓ Combined plot created")
        print("\n" + "=" * 80)
        print("✓ BOX AND VIOLIN PLOTS COMPLETE")
        print("=" * 80)
    
    return figures


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    from .data_loader import load_all_designs
    from .complexity_analyzer import analyze_design_complexity
    
    # Test box and violin plots
    design_dirs = get_sorted_designs(DATA_ROOT)
    all_designs_data = load_all_designs(design_dirs, verbose=False)
    complexity_results = analyze_design_complexity(all_designs_data, verbose=False)
    
    figures = create_all_box_violin_plots(complexity_results, verbose=True)
