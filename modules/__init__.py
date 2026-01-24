"""
UAV Network Analysis Modules
============================
Modular Python files for analyzing and visualizing UAV design networks.

Modules:
    - config: Configuration and paths
    - setup: Imports and initialization
    - data_loader: Load and parse design data
    - cad_plotter: Plot CAD models
    - geometry_parser: Parse design tree geometry
    - position_calculator: Calculate 3D positions
    - network_plotter: Network visualization
    - interactive_plotter: Interactive plots
    - complexity_analyzer: Complexity calculations
    - complexity_radar_plot: Radar/spider plots for complexity metrics
    - complexity_box_violin_plot: Box and violin plots for complexity distributions
    - design_selector: Select representative designs for analysis
    - plot_utils: Plotting utilities
"""

__version__ = "1.0.0"
__author__ = "Research Team"

# Make key functions available at package level
from .config import CONFIG, get_plots_dir, get_data_root
from .plot_utils import save_plot, save_and_show, save_figure

__all__ = [
    'CONFIG',
    'get_plots_dir',
    'get_data_root',
    'save_plot',
    'save_and_show',
    'save_figure',
]
