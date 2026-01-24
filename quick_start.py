"""
Quick Start Script
==================
This script demonstrates the basic workflow for UAV network analysis.
Run this to verify that all modules are working correctly.
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

# Import modules
from modules import config, setup, data_loader
from modules import geometry_parser, position_calculator
from modules import cad_plotter, network_plotter, complexity_analyzer

def main():
    """Run a quick analysis pipeline."""
    
    print("\n" + "=" * 80)
    print("UAV NETWORK ANALYSIS - QUICK START")
    print("=" * 80)
    
    # 1. Initialize
    print("\n[1/7] Initializing environment...")
    env_state = setup.initialize_environment()
    
    # 2. Get design directories
    print("\n[2/7] Finding design directories...")
    design_dirs = setup.get_sorted_designs(config.DATA_ROOT)
    
    if len(design_dirs) == 0:
        print("\n⚠ No designs found! Check DATA_ROOT in modules/config.py")
        return
    
    # 3. Load data
    print("\n[3/7] Loading design data...")
    all_designs_data = data_loader.load_all_designs(design_dirs, verbose=True)
    
    # 4. Parse geometry
    print("\n[4/7] Parsing geometry...")
    designs_geometry = geometry_parser.parse_all_geometries(all_designs_data, verbose=True)
    
    # 5. Calculate positions
    print("\n[5/7] Calculating 3D positions...")
    all_positions_3d = position_calculator.calculate_all_positions(
        all_designs_data, 
        designs_geometry, 
        verbose=True
    )
    
    # 6. Analyze complexity
    print("\n[6/7] Analyzing complexity...")
    complexity_results = complexity_analyzer.analyze_design_complexity(
        all_designs_data,
        verbose=True
    )
    
    # Print summary
    summary = complexity_analyzer.get_complexity_summary(complexity_results)
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Designs analyzed: {len(all_designs_data)}")
    print(f"Average complexity: {summary['total_complexity']['mean']:.3f} ± {summary['total_complexity']['std']:.3f} bits")
    print(f"Plots saved to: {config.PLOTS_DIR}")
    
    # 7. Create sample plot
    print("\n[7/7] Creating sample network plot...")
    first_design = sorted(all_designs_data.keys(), key=setup.get_design_number)[0]
    
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    network_plotter.plot_network_3d(
        all_designs_data[first_design]['G'],
        all_positions_3d[first_design],
        title=f"Sample: {first_design}",
        ax=ax,
        show_legend=True,
        save=True
    )
    
    print("\n" + "=" * 80)
    print("✓ QUICK START COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Open UAV_Network_Analysis_Main.ipynb in Jupyter")
    print("2. Run all blocks sequentially")
    print("3. Check plots/ directory for outputs")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
