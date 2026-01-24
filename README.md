# CHORD_Complexity_Analysis_Jan2026

# UAV Network Analysis - Organized Structure

A clean, modular Python framework for analyzing and visualizing UAV design networks with complexity metrics.

## Project Structure

```
organized_uav_analysis/
├── UAV_Network_Analysis_Main.ipynb    # Main Jupyter notebook
├── modules/                            # Python modules
│   ├── __init__.py                    # Package initialization
│   ├── config.py                      # Configuration and paths
│   ├── setup.py                       # Environment setup
│   ├── plot_utils.py                  # Plotting utilities
│   ├── data_loader.py                 # Load design data
│   ├── cad_plotter.py                 # CAD model visualization
│   ├── geometry_parser.py             # Parse design geometry
│   ├── position_calculator.py         # Calculate 3D positions
│   ├── network_plotter.py             # Network visualization
│   └── complexity_analyzer.py         # Complexity analysis
├── plots/                             # Output plots (auto-created)
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## Quick Start

### 1. Install Dependencies

```bash
cd organized_uav_analysis
pip install -r requirements.txt
```

### 2. Run the Main Notebook

Open `UAV_Network_Analysis_Main.ipynb` in Jupyter:

```bash
jupyter notebook UAV_Network_Analysis_Main.ipynb
```

### 3. Execute Blocks Sequentially

Run each block in order. The notebook will:
- Load all 15 UAV designs
- Generate CAD visualizations
- Create 3D network graphs
- Calculate complexity metrics
- Save all plots automatically

## Analysis Pipeline

### Block 1: Setup
- Initialize environment
- Load utilities
- Configure paths and settings

### Block 2: Load Design Data
- Parse JSON files
- Build network graphs
- Extract component information

### Block 3: CAD Visualization
- Plot 3D STL models
- Grid view of all designs

### Block 4: Verification
- Verify component extraction
- Check data integrity

### Block 5: Geometry Parsing
- Extract hub types
- Get arm lengths
- Parse sensor positions

### Block 6: Position Calculation
- Calculate realistic 3D positions
- Mimic CAD placement
- Position all components

### Block 7: Network Visualization
- Plot 3D network graphs
- Color-coded by component type
- All designs in grid layout

### Block 8: Selected Designs
- Pick representative samples
- Detailed visualization
- Comparison analysis

### Block 9: Complexity Analysis
- Shannon entropy calculations
- System-level metrics
- Node-level complexity

### Block 10: Comparison Plots
- Bar charts of complexity
- Diversity metrics
- Flexibility analysis

### Block 11: Complexity Distribution Plots
- Box plots with quartiles and outliers
- Violin plots showing distribution shape
- Combined box and violin plots

### Block 12: Complexity Radar Plots
- Radar/spider plots for multi-dimensional metrics
- Overview plot with all designs
- Grid of individual plots
- Grouped by complexity level

## Module Overview

### `config.py`
Central configuration for paths, colors, and settings. Modify this file to change:
- Data paths
- Plot output directory
- DPI and figure sizes
- Color schemes

### `data_loader.py`
Load and parse design data:
```python
from modules import data_loader
all_designs = data_loader.load_all_designs(design_dirs)
```

### `geometry_parser.py`
Extract geometric information:
```python
from modules import geometry_parser
geometry = geometry_parser.parse_all_geometries(all_designs)
```

### `position_calculator.py`
Calculate 3D node positions:
```python
from modules import position_calculator
positions = position_calculator.calculate_all_positions(all_designs, geometry)
```

### `network_plotter.py`
Create network visualizations:
```python
from modules import network_plotter
fig = network_plotter.plot_network_3d(G, positions)
```

### `complexity_analyzer.py`
Analyze structural complexity:
```python
from modules import complexity_analyzer
results = complexity_analyzer.analyze_design_complexity(all_designs)
```

### `complexity_radar_plot.py`
Create radar/spider plots for multi-dimensional complexity:
```python
from modules import complexity_radar_plot
radar_data = complexity_radar_plot.prepare_radar_data(results, component_type='Motor')
fig = complexity_radar_plot.plot_radar_overview(radar_data, sorted_design_names)
```

### `complexity_box_violin_plot.py`
Create box and violin plots for complexity distributions:
```python
from modules import complexity_box_violin_plot
box_data, labels, stats = complexity_box_violin_plot.prepare_box_plot_data(results)
fig = complexity_box_violin_plot.plot_violin_with_box(box_data, labels, stats)
```

## Output

All plots are automatically saved to `plots/` directory in:
- **PNG** format (600 DPI, high resolution)
- **PDF** format (600 DPI, publication quality)

Files are date-stamped for version control.

## Customization

### Change Plot Settings
Edit `modules/config.py`:
```python
PLOT_CONFIG = {
    'dpi': 600,              # Change resolution
    'figsize_default': (18, 18),  # Change figure size
    'font_size_default': 12,      # Change font size
}
```

### Change Color Scheme
Edit `COLOR_MAP` in `modules/config.py`:
```python
COLOR_MAP = {
    'MainHub': '#FF6B6B',    # Red
    'Motor': '#45B7D1',      # Blue
    'Sensor': '#FFD93D',     # Yellow
    # ... add more
}
```

### Change Output Directory
```python
from modules import config
config.update_plots_dir('/path/to/new/directory')
```

## Testing Modules

Each module can be tested independently:

```bash
# Test data loader
python -m modules.data_loader

# Test geometry parser
python -m modules.geometry_parser

# Test complexity analyzer
python -m modules.complexity_analyzer
```


