# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational Python repository designed for WGU's Master of Science in Software Engineering - AI Engineering program. It focuses on teaching data structures (Lists, Dictionaries, Sets) through Jupyter notebooks with practical exercises.

## Development Setup

### Environment Management

- **Python Version**: 3.12 (specified in `.python-version`)
- **Package Manager**: UV (modern Python package manager)
- **Virtual Environment**: `.venv` directory

### Common Commands

```bash
# Setup environment
uv venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install dependencies (currently none, but for future additions)
uv pip install jupyter

# Start Jupyter for exercises
jupyter notebook
```

## Known Issues

### ✅ RESOLVED: Jupyter Notebook JSON Syntax Errors

**Fixed Issues (2024-07-07)**:

- `01_lists_basics.ipynb` - Fixed extra closing braces in JSON structure (lines 57, 112)
- `03_sets_basics.ipynb` - Fixed extra closing braces in JSON structure (lines 70, 127)

**Remaining Issues**:

- Notebooks still contain incomplete variable assignments (e.g., `songs = None` placeholders)
- These are intentional for educational purposes - students fill in the solutions

### Missing Implementation

- `main.py` is currently just a placeholder
- No test framework or linting setup
- Empty dependencies in `pyproject.toml`

## Architecture & Structure

### Learning Path

1. **01_lists_basics.ipynb** - Foundation list operations (slicing, indexing)
2. **02_dictionaries_basics.ipynb** - Key-value mappings and lookups
3. **03_sets_basics.ipynb** - Unique collections and set operations
4. **04_combined_practice.ipynb** - Integration of all three structures
5. **05_ai_scenarios.ipynb** - AI/ML relevant applications

### Data Files

- `data/sample_data.json` - Contains music playlist data and AI model metadata
- Note: AI model parameters are stored as strings ("1.7T") rather than numeric values

### Solutions

- `solutions/01_lists_solutions.md` - Complete solutions with multiple approaches
- Solutions demonstrate both comprehension and traditional loop approaches

## Development Priorities

When working on this codebase:

1. **✅ Notebook JSON syntax fixed** - All notebooks now load properly in Jupyter
2. **Consider adding dependencies**: `jupyter`, `pytest` for testing
3. **Enhance main.py** if adding interactive features or exercise runners
4. **Maintain ADHD-friendly approach**: Keep exercises to 30-45 minute sessions

## Educational Context

This repository is specifically designed for ADHD learners with:

- Short, focused exercises
- Clear visual separation of concepts
- Multiple solution approaches
- Step-by-step progression

The exercises use real-world scenarios (music playlists, student records, AI models) to maintain engagement and practical relevance.
