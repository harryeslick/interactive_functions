#!/usr/bin/env python3
"""
Deployment validation script for Pyodide marimo notebooks.

This script checks that all required assets are in place for successful
Pyodide deployment of marimo notebooks.
"""

import sys
from pathlib import Path
from urllib.parse import urljoin
import zipfile


def check_wheel_file():
    """Check that the wheel file exists and is valid."""
    wheel_path = Path("docs/assets/wheels/interactive_functions-latest-py3-none-any.whl")
    
    if not wheel_path.exists():
        print(f"❌ Wheel file missing: {wheel_path}")
        return False
    
    print(f"✅ Wheel file exists: {wheel_path}")
    print(f"   Size: {wheel_path.stat().st_size} bytes")
    
    # Validate wheel structure
    try:
        with zipfile.ZipFile(wheel_path, 'r') as z:
            files = z.namelist()
            # Check for key files
            has_init = any('__init__.py' in f for f in files)
            has_metadata = any('METADATA' in f for f in files)
            
            if has_init and has_metadata:
                print("   ✅ Wheel structure is valid")
                return True
            else:
                print("   ❌ Wheel structure is invalid")
                return False
                
    except zipfile.BadZipFile:
        print("   ❌ Wheel file is corrupted")
        return False


def check_marimo_files():
    """Check that marimo files have Pyodide compatibility."""
    marimo_files = ["dispersal_kernels_marimo.py", "diminishing_marimo.py"]
    all_good = True
    
    for filename in marimo_files:
        filepath = Path(filename)
        if not filepath.exists():
            print(f"❌ Marimo file missing: {filename}")
            all_good = False
            continue
            
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check for required patterns
        checks = [
            ('emscripten check', 'sys.platform == "emscripten"'),
            ('wheel_url construction', 'wheel_url = urljoin('),
            ('micropip install', 'await micropip.install('),
            ('interactive_functions import', 'import interactive_functions')
        ]
        
        file_ok = True
        print(f"✅ Checking {filename}:")
        
        for check_name, pattern in checks:
            if pattern in content:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                file_ok = False
                
        if not file_ok:
            all_good = False
            
    return all_good


def check_url_patterns():
    """Verify URL construction works correctly."""
    base_href = "https://harryeslick.github.io/interactive_functions/examples/dispersal_kernels/"
    if not base_href.endswith("/"):
        base_href += "/"
    wheel_url = urljoin(base_href, "assets/wheels/interactive_functions-latest-py3-none-any.whl")
    
    expected_url = "https://harryeslick.github.io/interactive_functions/examples/dispersal_kernels/assets/wheels/interactive_functions-latest-py3-none-any.whl"
    
    if wheel_url == expected_url:
        print("✅ URL construction works correctly")
        print(f"   Generated: {wheel_url}")
        return True
    else:
        print("❌ URL construction failed")
        print(f"   Generated: {wheel_url}")
        print(f"   Expected:  {expected_url}")
        return False


def main():
    """Run all validation checks."""
    print("🔍 Pyodide Deployment Validation")
    print("=" * 40)
    
    checks = [
        ("Wheel file validation", check_wheel_file),
        ("Marimo files validation", check_marimo_files),
        ("URL pattern validation", check_url_patterns),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}")
        result = check_func()
        if not result:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All validation checks passed!")
        print("📦 Deployment should work correctly")
        return 0
    else:
        print("💥 Some validation checks failed!")
        print("🔧 Please fix the issues before deployment")
        return 1


if __name__ == "__main__":
    sys.exit(main())