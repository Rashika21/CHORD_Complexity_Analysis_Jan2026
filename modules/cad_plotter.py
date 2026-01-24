"""
CAD Model Plotter
=================
Plot 3D CAD models from STL files.
"""

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh
from pathlib import Path

from .setup import get_design_number
from .plot_utils import save_and_show
from .config import CONFIG


def plot_single_cad_model(design_dir, ax=None, show_axes=True):
    """
    Plot STL CAD file for a single design.
    
    Parameters:
    -----------
    design_dir : Path
        Design directory containing cadfile.stl
    ax : matplotlib 3D axes, optional
        Axes to plot on. If None, creates new figure
    show_axes : bool
        Whether to show axis labels
        
    Returns:
    --------
    ax
        The axes object
    """
    if ax is None:
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='3d')
    
    stl_path = design_dir / 'cadfile.stl'
    
    if stl_path.exists():
        try:
            # Load and flip Z-axis
            your_mesh = mesh.Mesh.from_file(str(stl_path))
            your_mesh.vectors[:, :, -1] = -your_mesh.vectors[:, :, -1]
            
            # Add to plot
            ax.add_collection3d(mplot3d.art3d.Poly3DCollection(
                your_mesh.vectors, alpha=0.3, edgecolor='gray'
            ))
            
            # Scale axes
            scale = your_mesh.points.flatten()
            ax.auto_scale_xyz(scale, scale, scale)
            
            # Set labels
            if show_axes:
                ax.set_title(f'{design_dir.name}', fontsize=16, fontweight='bold', pad=10)
                ax.set_xlabel('X', fontsize=12)
                ax.set_ylabel('Y', fontsize=12)
                ax.set_zlabel('Z', fontsize=12)
            
        except Exception as e:
            ax.text(0.5, 0.5, 0.5, f"Error:\n{str(e)[:30]}",
                    ha='center', va='center', fontsize=10)
            if show_axes:
                ax.set_title(f'{design_dir.name}\n(Error)', fontsize=14)
    else:
        ax.text(0.5, 0.5, 0.5, "No STL", ha='center', va='center', fontsize=12)
        if show_axes:
            ax.set_title(f'{design_dir.name}\n(No STL)', fontsize=14)
    
    return ax


def plot_all_cad_models(design_dirs, n_cols=5, save=True, dpi=None):
    """
    Plot STL CAD files for all designs in a grid (ascending order).
    
    Parameters:
    -----------
    design_dirs : list
        List of design directories
    n_cols : int
        Number of columns in grid (default: 5)
    save : bool
        Whether to save the plot
    dpi : int, optional
        DPI for saving (default: from CONFIG)
        
    Returns:
    --------
    fig
        The figure object
    """
    if dpi is None:
        dpi = CONFIG['plotting']['dpi']
    
    print("\n" + "=" * 80)
    print("PLOTTING CAD MODELS FOR ALL DESIGNS")
    print("=" * 80)
    
    # Sort designs in ascending order by design number
    sorted_designs = sorted(design_dirs, key=get_design_number)
    
    n_designs = len(sorted_designs)
    n_rows = (n_designs + n_cols - 1) // n_cols
    
    fig = plt.figure(figsize=(24, 6 * n_rows))
    
    for idx, design_dir in enumerate(sorted_designs):
        ax = fig.add_subplot(n_rows, n_cols, idx + 1, projection='3d')
        plot_single_cad_model(design_dir, ax=ax, show_axes=True)
    
    plt.suptitle(f'CAD Models - All {n_designs} Designs', 
                 fontsize=30, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if save:
        save_and_show(fig, 'CAD_Models_All15', dpi=dpi)
    
    print(f"✓ CAD models plotted for all {len(design_dirs)} designs")
    
    return fig


def plot_cad_comparison(design_dirs, design_indices, titles=None, save=True):
    """
    Plot CAD models for specific designs for comparison.
    
    Parameters:
    -----------
    design_dirs : list
        List of all design directories
    design_indices : list
        Indices of designs to plot
    titles : list, optional
        Custom titles for each subplot
    save : bool
        Whether to save the plot
        
    Returns:
    --------
    fig
        The figure object
    """
    n_designs = len(design_indices)
    n_cols = min(n_designs, 4)
    n_rows = (n_designs + n_cols - 1) // n_cols
    
    fig = plt.figure(figsize=(6 * n_cols, 6 * n_rows))
    
    for i, idx in enumerate(design_indices):
        ax = fig.add_subplot(n_rows, n_cols, i + 1, projection='3d')
        design_dir = design_dirs[idx]
        plot_single_cad_model(design_dir, ax=ax, show_axes=True)
        
        if titles and i < len(titles):
            ax.set_title(titles[i], fontsize=14, fontweight='bold')
    
    plt.suptitle('Selected CAD Models Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save:
        save_and_show(fig, 'CAD_Models_Comparison')
    
    return fig


if __name__ == "__main__":
    from .config import DATA_ROOT
    from .setup import get_sorted_designs
    
    # Test CAD plotting
    design_dirs = get_sorted_designs(DATA_ROOT)
    if len(design_dirs) > 0:
        # Plot all CAD models
        fig = plot_all_cad_models(design_dirs)
        print("✓ CAD plotting test completed")
    else:
        print("⚠ No designs found")
