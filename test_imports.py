"""
Test Imports
============
Quick script to verify all modules can be imported without errors.
Run this first to check that the environment is set up correctly.
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

print("=" * 80)
print("TESTING MODULE IMPORTS")
print("=" * 80)

errors = []

# Test each module import
modules_to_test = [
    ('config', 'Configuration'),
    ('setup', 'Setup'),
    ('plot_utils', 'Plot Utilities'),
    ('data_loader', 'Data Loader'),
    ('cad_plotter', 'CAD Plotter'),
    ('geometry_parser', 'Geometry Parser'),
    ('position_calculator', 'Position Calculator'),
    ('network_plotter', 'Network Plotter'),
    ('complexity_analyzer', 'Complexity Analyzer'),
]

for module_name, display_name in modules_to_test:
    try:
        exec(f"from modules import {module_name}")
        print(f"✓ {display_name:30s} ... OK")
    except Exception as e:
        print(f"✗ {display_name:30s} ... FAILED")
        errors.append((display_name, str(e)))

print("\n" + "=" * 80)

if errors:
    print("ERRORS FOUND:")
    print("=" * 80)
    for module, error in errors:
        print(f"\n{module}:")
        print(f"  {error}")
    print("\n" + "=" * 80)
    print("⚠ Some modules failed to import. Check error messages above.")
else:
    print("✓ ALL MODULES IMPORTED SUCCESSFULLY!")
    print("=" * 80)
    print("\nYou can now:")
    print("  1. Run: python quick_start.py")
    print("  2. Open: UAV_Network_Analysis_Main.ipynb")

print("=" * 80)
