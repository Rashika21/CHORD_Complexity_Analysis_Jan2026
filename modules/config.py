"""
Configuration and Path Management
=================================
Central configuration for all paths and settings.
"""

from pathlib import Path
from datetime import datetime

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

# Base paths
BASE_DIR = Path(__file__).parent.parent
ROOT = Path("/Users/RashikaSN/Rashika/01 Education/01 Education/03 Stevens/00 Research/11 Complexity/Aircraft Copter Data/AircraftVerse Github/AircraftVerse")
DATA_ROOT = ROOT / "data"  # 15 designs folder
UTIL_PATH = ROOT / "code"

# Output paths
PLOTS_DIR = BASE_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

# ============================================================================
# PLOTTING CONFIGURATION
# ============================================================================

PLOT_CONFIG = {
    'dpi': 600,
    'figsize_default': (18, 18),
    'figsize_3d': (24, 18),
    'figsize_grid': (24, 18),
    'font_size_default': 12,
    'font_size_title': 14,
    'font_size_label': 10,
    'save_formats': ['png', 'pdf'],
    'bbox_inches': 'tight',
    'pad_inches': 0.3,
}

# ============================================================================
# NETWORK VISUALIZATION CONFIGURATION
# ============================================================================

COLOR_MAP = {
    'MainHub': '#FF6B6B',
    'Arm': '#4ECDC4',
    'Motor': '#45B7D1',
    'Propeller': '#FFA07A',
    'Flange': '#98D8C8',
    'Tube': '#C7CEEA',
    'Sensor': '#FFD93D',
    'Battery': '#6BCB77',
    'Fuselage': '#D4A5A5',
    'BatteryController': '#9D84B7',
    'LandingGear': '#A8E6CF',
    'Default': '#CCCCCC',
}

NETWORK_CONFIG = {
    'node_size': 1000,
    'node_alpha': 0.95,
    'edge_alpha': 0.5,
    'edge_width': 1.2,
    'arrow_size': 25,
    'connection_style': 'arc3,rad=0.12',
    'linewidths': 2.5,
}

# ============================================================================
# COMPLEXITY ANALYSIS CONFIGURATION
# ============================================================================

COMPLEXITY_CONFIG = {
    'entropy_base': 2,  # Base for Shannon entropy
    'normalization': True,
    'min_connections': 1,
}

# ============================================================================
# GENERAL CONFIGURATION
# ============================================================================

CONFIG = {
    'paths': {
        'root': ROOT,
        'data_root': DATA_ROOT,
        'util_path': UTIL_PATH,
        'plots_dir': PLOTS_DIR,
        'base_dir': BASE_DIR,
    },
    'plotting': PLOT_CONFIG,
    'colors': COLOR_MAP,
    'network': NETWORK_CONFIG,
    'complexity': COMPLEXITY_CONFIG,
    'date': datetime.now().strftime("%Y-%m-%d"),
    'timestamp': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_plots_dir():
    """Get plots directory, creating if needed."""
    PLOTS_DIR.mkdir(exist_ok=True)
    return PLOTS_DIR

def get_data_root():
    """Get data root directory."""
    return DATA_ROOT

def get_color_map():
    """Get color map for components."""
    return COLOR_MAP.copy()

def update_plots_dir(new_path):
    """Update plots directory."""
    global PLOTS_DIR
    PLOTS_DIR = Path(new_path)
    PLOTS_DIR.mkdir(exist_ok=True)
    CONFIG['paths']['plots_dir'] = PLOTS_DIR
    return PLOTS_DIR

# ============================================================================
# DISPLAY CONFIGURATION
# ============================================================================

def print_config():
    """Print current configuration."""
    print("=" * 80)
    print("UAV NETWORK ANALYSIS - CONFIGURATION")
    print("=" * 80)
    print(f"\n📁 Paths:")
    print(f"   Root:        {ROOT}")
    print(f"   Data:        {DATA_ROOT}")
    print(f"   Plots:       {PLOTS_DIR}")
    print(f"\n🎨 Plotting:")
    print(f"   DPI:         {PLOT_CONFIG['dpi']}")
    print(f"   Formats:     {', '.join(PLOT_CONFIG['save_formats'])}")
    print(f"\n📅 Date:        {CONFIG['date']}")
    print("=" * 80)

if __name__ == "__main__":
    print_config()
