# Installation Guide - Python Data Structures Practice

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://chevyphillip.github.io/python-data-structures-practice/)
[![Repository](https://img.shields.io/badge/repo-GitHub-blue)](https://github.com/chevyphillip/python-data-structures-practice)

**🌐 Live Documentation:** [https://chevyphillip.github.io/python-data-structures-practice/](https://chevyphillip.github.io/python-data-structures-practice/)

This guide provides instructions for setting up the project dependencies using both **uv** (recommended) and **pip** package managers.

## Prerequisites

- **Python 3.12+** (required)
- **uv** package manager (recommended) or **pip**

## Quick Start (Recommended - Using uv)

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### 2. Set up the project

```bash
# Clone/navigate to project directory
cd python-data-structures-practice

# Create virtual environment and install dependencies
uv sync

# Install development dependencies (optional)
uv sync --extra dev

# Install enhanced dependencies (optional)
uv sync --extra enhanced

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### 3. Start Jupyter Notebook

```bash
jupyter notebook
```

## Alternative Setup (Using pip)

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### 2. Install dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Or install from pyproject.toml
pip install -e .

# Install development dependencies
pip install -e .[dev]

# Install enhanced dependencies
pip install -e .[enhanced]
```

### 3. Start Jupyter Notebook

```bash
jupyter notebook
```

## Dependency Categories

### Core Dependencies (Always Installed)

- **notebook==7.4.4** - Jupyter notebook interface
- **ipykernel>=6.29.0** - Python kernel for Jupyter

### Development Dependencies (Optional - `dev` extra)

- **pytest==8.4.1** - Testing framework
- **black>=24.0.0** - Code formatter
- **flake8>=7.0.0** - Linting tool
- **mypy>=1.8.0** - Type checking

### Enhanced Dependencies (Optional - `enhanced` extra)

- **jupyterlab>=4.0.0** - Modern Jupyter interface
- **ipywidgets>=8.0.0** - Interactive widgets

## Verification

Run the verification script to ensure everything is working:

```bash
python verify_requirements.py
```

## Common Commands

### Using uv (Recommended)

```bash
# Install/update all dependencies
uv sync

# Install with development tools
uv sync --extra dev

# Install with enhanced features
uv sync --extra enhanced

# Add a new dependency
uv add package-name

# Remove a dependency
uv remove package-name

# Run Jupyter
uv run jupyter notebook
```

### Using pip

```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .[dev,enhanced]

# Freeze current dependencies
pip freeze > requirements-lock.txt
```

## Troubleshooting

### Python Version Issues

Ensure you're using Python 3.12+:

```bash
python --version
```

### Virtual Environment Issues

If you encounter issues, try recreating the virtual environment:

```bash
# Remove existing environment
rm -rf .venv

# Recreate with uv
uv sync

# Or with pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Jupyter Kernel Issues

If Jupyter can't find the Python kernel:

```bash
# Install kernel manually
python -m ipykernel install --user --name=python-data-structures

# List available kernels
jupyter kernelspec list
```

## Version Pinning Strategy

- **notebook** and **pytest**: Pinned to specific versions for consistency
- **Other packages**: Use minimum version constraints (>=) for flexibility
- **All versions**: Compatible with Python 3.12+ requirement

This approach balances stability with flexibility, allowing for security updates while maintaining compatibility.

---

**🌐 For the latest documentation and updates, visit:** [https://chevyphillip.github.io/python-data-structures-practice/](https://chevyphillip.github.io/python-data-structures-practice/)

**📂 Repository:** [https://github.com/chevyphillip/python-data-structures-practice](https://github.com/chevyphillip/python-data-structures-practice)
