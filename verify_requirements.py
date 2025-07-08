#!/usr/bin/env python3
"""
Verification script for requirements.txt compatibility
Tests both pip and uv package managers
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔍 {description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ SUCCESS")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Error: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print("❌ COMMAND NOT FOUND")
        return False

def main():
    """Main verification function"""
    print("🚀 Python Data Structures Practice - Requirements Verification")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found. Please run from project root.")
        sys.exit(1)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 12):
        print("⚠️  WARNING: Python 3.12+ is required by this project")
    
    # Test uv commands
    print("\n" + "=" * 60)
    print("TESTING UV PACKAGE MANAGER")
    print("=" * 60)
    
    uv_tests = [
        (["uv", "--version"], "Check uv version"),
        (["uv", "pip", "install", "--dry-run", "-r", "requirements.txt"], "Test requirements.txt with uv"),
        (["uv", "sync", "--dry-run"], "Test pyproject.toml sync with uv"),
        (["uv", "sync", "--dry-run", "--extra", "dev"], "Test dev dependencies with uv"),
        (["uv", "sync", "--dry-run", "--extra", "enhanced"], "Test enhanced dependencies with uv"),
    ]
    
    uv_success = 0
    for cmd, desc in uv_tests:
        if run_command(cmd, desc):
            uv_success += 1
    
    print(f"\n📊 UV Tests: {uv_success}/{len(uv_tests)} passed")
    
    # Test pip commands (if available)
    print("\n" + "=" * 60)
    print("TESTING PIP COMPATIBILITY")
    print("=" * 60)
    
    pip_tests = [
        (["pip", "--version"], "Check pip version"),
        (["pip", "install", "--dry-run", "-r", "requirements.txt"], "Test requirements.txt with pip"),
    ]
    
    pip_success = 0
    for cmd, desc in pip_tests:
        if run_command(cmd, desc):
            pip_success += 1
    
    print(f"\n📊 PIP Tests: {pip_success}/{len(pip_tests)} passed")
    
    # Test Jupyter functionality
    print("\n" + "=" * 60)
    print("TESTING JUPYTER FUNCTIONALITY")
    print("=" * 60)
    
    jupyter_tests = [
        (["jupyter", "--version"], "Check Jupyter installation"),
        (["jupyter", "kernelspec", "list"], "List available kernels"),
    ]
    
    jupyter_success = 0
    for cmd, desc in jupyter_tests:
        if run_command(cmd, desc):
            jupyter_success += 1
    
    print(f"\n📊 Jupyter Tests: {jupyter_success}/{len(jupyter_tests)} passed")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    total_tests = len(uv_tests) + len(pip_tests) + len(jupyter_tests)
    total_success = uv_success + pip_success + jupyter_success
    
    print(f"Overall Success Rate: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    
    if total_success == total_tests:
        print("🎉 All tests passed! Your requirements are properly configured.")
    elif uv_success == len(uv_tests):
        print("✅ UV tests passed. Your project is ready for uv-based development.")
        if pip_success < len(pip_tests):
            print("ℹ️  Note: Some pip tests failed, but this is expected in uv-only environments.")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    
    return total_success == total_tests or uv_success == len(uv_tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
