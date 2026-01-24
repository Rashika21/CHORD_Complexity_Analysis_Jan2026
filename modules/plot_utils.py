"""
Plotting Utilities
==================
Functions for saving and displaying plots.
"""

import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from .config import CONFIG, PLOTS_DIR


def save_plot(fig, filename, dpi=None, format='png', bbox_inches='tight', pad_inches=0.3):
    """
    Save a matplotlib figure to high-resolution file.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to save
    filename : str
        Filename (without extension)
    dpi : int, optional
        Resolution in dots per inch (default: from CONFIG)
    format : str
        File format: 'png', 'pdf', 'svg', 'jpg' (default: 'png')
    bbox_inches : str
        Bounding box: 'tight' to remove extra whitespace
    pad_inches : float
        Padding around the plot
        
    Returns:
    --------
    Path
        Path to saved file
    """
    if dpi is None:
        dpi = CONFIG['plotting']['dpi']
    
    filepath = PLOTS_DIR / f"{filename}.{format}"
    fig.savefig(filepath, dpi=dpi, format=format, bbox_inches=bbox_inches, 
                pad_inches=pad_inches, facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: {filepath.name} ({format.upper()}, {dpi} DPI)")
    return filepath


def save_and_show(fig, filename=None, dpi=None, show=True):
    """
    Save a figure in multiple formats and optionally show it.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to save
    filename : str, optional
        Filename (without extension). If None, auto-generates from title
    dpi : int, optional
        Resolution in dots per inch (default: from CONFIG)
    show : bool
        Whether to call plt.show() after saving (default: True)
        
    Returns:
    --------
    str
        Filename used for saving
    """
    if dpi is None:
        dpi = CONFIG['plotting']['dpi']
    
    if filename is None:
        # Auto-generate filename from title
        try:
            if fig._suptitle is not None:
                title = fig._suptitle.get_text()
            elif len(fig.axes) > 0 and fig.axes[0].get_title() != '':
                title = fig.axes[0].get_title()
            else:
                title = f"figure_{fig.number}"
            
            filename = title.replace('\n', '_').replace(' ', '_')
            filename = ''.join(c for c in filename if c.isalnum() or c in ('_', '-'))
            filename = filename[:100]
            if not filename:
                filename = f"figure_{fig.number}"
        except:
            filename = f"figure_{fig.number}"
    
    # Save in configured formats
    for fmt in CONFIG['plotting']['save_formats']:
        save_plot(fig, filename, dpi=dpi, format=fmt)
    
    if show:
        plt.show()
    
    return filename


def save_figure(fig, name, dpi=None):
    """
    Save matplotlib figure with date-stamped filenames.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to save
    name : str
        Base name for the file
    dpi : int, optional
        Resolution (default: from CONFIG)
    """
    if dpi is None:
        dpi = CONFIG['plotting']['dpi']
    
    today = CONFIG['date']
    
    for fmt in CONFIG['plotting']['save_formats']:
        filepath = PLOTS_DIR / f"{today}_{name}.{fmt}"
        fig.savefig(filepath, dpi=dpi, bbox_inches="tight", pad_inches=0.2)
        print(f"  ✓ Saved: {filepath.name}")


def fix_legend_overlap(ax, loc='best', bbox_to_anchor=None, ncol=1, fontsize=None):
    """
    Fix legend overlapping with plot by adjusting position and layout.
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes object
    loc : str
        Legend location (default: 'best')
    bbox_to_anchor : tuple, optional
        Custom position (x, y) in axes coordinates
    ncol : int
        Number of columns for legend (default: 1)
    fontsize : int, optional
        Font size for legend
        
    Returns:
    --------
    tuple or None
        bbox_to_anchor coordinates
    """
    # Determine best position to avoid overlap
    if bbox_to_anchor is None:
        # Try to place legend outside plot area
        if loc in ['upper right', 'right', 'center right']:
            bbox_to_anchor = (1.02, 1) if 'upper' in loc else (1.02, 0.5)
        elif loc in ['upper left', 'left', 'center left']:
            bbox_to_anchor = (-0.02, 1) if 'upper' in loc else (-0.02, 0.5)
        elif loc in ['lower right']:
            bbox_to_anchor = (1.02, 0)
        elif loc in ['lower left']:
            bbox_to_anchor = (-0.02, 0)
        else:
            bbox_to_anchor = None
    
    # Adjust subplot to make room for legend
    if bbox_to_anchor is not None:
        if bbox_to_anchor[0] > 1:  # Legend on right
            plt.subplots_adjust(right=0.85)
        elif bbox_to_anchor[0] < 0:  # Legend on left
            plt.subplots_adjust(left=0.15)
    
    return bbox_to_anchor


def create_legend(ax, G, color_map, loc='upper left', fontsize=12):
    """
    Create a component type legend for network plot.
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes object
    G : networkx.Graph
        Network graph
    color_map : dict
        Component type to color mapping
    loc : str
        Legend location
    fontsize : int
        Font size for legend
    """
    from matplotlib.patches import Patch
    import networkx as nx
    
    component_types = set(nx.get_node_attributes(G, "component_type").values())
    legend_elements = [
        Patch(facecolor=color_map.get(comp_type, "#cccccc"), label=comp_type)
        for comp_type in sorted(component_types)
    ]
    ax.legend(handles=legend_elements, loc=loc, fontsize=fontsize,
              framealpha=0.95, title='Component Types', title_fontsize=fontsize+1)


def setup_plot_style():
    """Configure matplotlib style settings."""
    plt.style.use('default')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['font.size'] = CONFIG['plotting']['font_size_default']
    print("✓ Plot style configured")
