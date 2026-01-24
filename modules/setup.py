"""
Setup and Imports
=================
Initialize environment and import required libraries.
"""

import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
from pathlib import Path
import math
from stl import mesh
from matplotlib.patches import Patch
from collections import Counter, defaultdict
import sys
import os
from datetime import datetime

# Conditional imports
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠ Plotly not available. Interactive plots will be disabled.")

from .config import CONFIG, UTIL_PATH


def initialize_environment():
    """
    Initialize the analysis environment.
    
    Returns:
    --------
    dict
        Environment status and utilities
    """
    print("=" * 80)
    print("INITIALIZING UAV NETWORK ANALYSIS ENVIRONMENT")
    print("=" * 80)
    
    # Add util path
    sys.path.append(str(UTIL_PATH))
    
    # Try to import util functions
    util_available = False
    util_functions = {}
    
    try:
        from util import collect_design_parts, plot_stl, plot_pointCloud
        util_available = True
        util_functions = {
            'collect_design_parts': collect_design_parts,
            'plot_stl': plot_stl,
            'plot_pointCloud': plot_pointCloud,
        }
        print("✓ Util functions loaded successfully")
    except ImportError as e:
        print(f"⚠ Util functions not available: {e}")
    
    # Print configuration
    print(f"\n📁 Data root: {CONFIG['paths']['data_root']}")
    print(f"📁 Plots dir: {CONFIG['paths']['plots_dir']}")
    print(f"📅 Date: {CONFIG['date']}")
    
    # Check plotly
    if PLOTLY_AVAILABLE:
        print("✓ Plotly available for interactive plots")
    else:
        print("⚠ Plotly not available")
    
    print("=" * 80)
    
    return {
        'util_available': util_available,
        'util_functions': util_functions,
        'plotly_available': PLOTLY_AVAILABLE,
    }


def get_design_number(design_dir_or_name):
    """
    Extract number from design_1, design_2, etc. for sorting.
    
    Parameters:
    -----------
    design_dir_or_name : Path or str
        Design directory or name
        
    Returns:
    --------
    int
        Design number for sorting
    """
    if isinstance(design_dir_or_name, Path):
        name = design_dir_or_name.name
    else:
        name = str(design_dir_or_name)
    
    # Extract number after 'design_'
    try:
        if 'design_' in name:
            num_str = name.split('design_')[1].split('_')[0]
            return int(num_str)
        return 999  # Fallback for non-standard names
    except:
        return 999


def get_sorted_designs(data_root):
    """
    Get sorted list of design directories.
    
    Parameters:
    -----------
    data_root : Path
        Root directory containing design folders
        
    Returns:
    --------
    list
        Sorted list of design Path objects
    """
    design_dirs = sorted(
        [d for d in data_root.iterdir() if d.is_dir() and d.name.startswith('design_')],
        key=get_design_number
    )
    
    print(f"\n📦 Found {len(design_dirs)} designs in data folder (sorted 1-{len(design_dirs)})")
    for i, d in enumerate(design_dirs, 1):
        print(f"  {i:2d}. {d.name}")
    
    return design_dirs


# Global state for utilities
_env_state = None

def get_env_state():
    """Get environment state, initializing if needed."""
    global _env_state
    if _env_state is None:
        _env_state = initialize_environment()
    return _env_state


if __name__ == "__main__":
    # Test initialization
    env = initialize_environment()
    print("\nEnvironment status:")
    for key, value in env.items():
        print(f"  {key}: {value}")
