#!/usr/bin/env python3
"""
Content Validator for Python Data Structures Learning Framework

This tool validates that exercises meet quality standards and ADHD-friendly design principles.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
import nbformat
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Results from content validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]


class ContentValidator:
    """Validates learning content for quality and consistency."""
    
    def __init__(self):
        self.adhd_guidelines = {
            'max_cell_lines': 20,  # Maximum lines per code cell
            'max_exercise_cells': 8,  # Maximum cells per exercise
            'required_sections': ['instructions', 'hint', 'solution_space'],
            'estimated_time_max': 60,  # Maximum minutes for beginner exercises
        }
    
    def validate_notebook(self, notebook_path: Path) -> ValidationResult:
        """Validate a Jupyter notebook exercise."""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
        except Exception as e:
            return ValidationResult(False, [f"Failed to read notebook: {e}"], [], [])
        
        errors = []
        warnings = []
        suggestions = []
        
        # Check notebook structure
        structure_result = self._check_notebook_structure(nb)
        errors.extend(structure_result.errors)
        warnings.extend(structure_result.warnings)
        suggestions.extend(structure_result.suggestions)
        
        # Check ADHD-friendly design
        adhd_result = self._check_adhd_friendly_design(nb)
        errors.extend(adhd_result.errors)
        warnings.extend(adhd_result.warnings)
        suggestions.extend(adhd_result.suggestions)
        
        # Check code quality
        code_result = self._check_code_quality(nb)
        errors.extend(code_result.errors)
        warnings.extend(code_result.warnings)
        suggestions.extend(code_result.suggestions)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def _check_notebook_structure(self, nb: nbformat.NotebookNode) -> ValidationResult:
        """Check that notebook has proper structure."""
        errors = []
        warnings = []
        suggestions = []
        
        cells = nb.cells
        if len(cells) < 3:
            errors.append("Notebook must have at least 3 cells (title, exercise, solution)")
        
        # Check for title cell
        first_cell = cells[0] if cells else None
        if not first_cell or first_cell.cell_type != 'markdown':
            errors.append("First cell must be markdown with title and description")
        elif first_cell.cell_type == 'markdown':
            title_content = first_cell.source.lower()
            if 'goal:' not in title_content:
                warnings.append("Title cell should include learning goal")
            if 'time:' not in title_content:
                warnings.append("Title cell should include estimated time")
        
        # Check exercise structure
        has_instructions = False
        has_code_cell = False
        
        for cell in cells:
            if cell.cell_type == 'markdown' and any(keyword in cell.source.lower() 
                                                   for keyword in ['instructions', 'tasks']):
                has_instructions = True
            elif cell.cell_type == 'code':
                has_code_cell = True
        
        if not has_instructions:
            errors.append("Notebook must include clear instructions for exercises")
        if not has_code_cell:
            errors.append("Notebook must include code cells for student solutions")
        
        return ValidationResult(len(errors) == 0, errors, warnings, suggestions)
    
    def _check_adhd_friendly_design(self, nb: nbformat.NotebookNode) -> ValidationResult:
        """Check ADHD-friendly design principles."""
        errors = []
        warnings = []
        suggestions = []
        
        code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
        
        # Check code cell length
        for i, cell in enumerate(code_cells):
            lines = len(cell.source.split('\n'))
            if lines > self.adhd_guidelines['max_cell_lines']:
                warnings.append(f"Code cell {i+1} has {lines} lines (recommend max {self.adhd_guidelines['max_cell_lines']})")
        
        # Check total number of exercises
        exercise_pattern = re.compile(r'##\s*Exercise\s*\d+', re.IGNORECASE)
        exercise_count = 0
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                exercise_count += len(exercise_pattern.findall(cell.source))
        
        if exercise_count > self.adhd_guidelines['max_exercise_cells']:
            warnings.append(f"Notebook has {exercise_count} exercises (recommend max {self.adhd_guidelines['max_exercise_cells']})")
        
        # Check for visual hierarchy
        markdown_cells = [cell for cell in nb.cells if cell.cell_type == 'markdown']
        has_headers = False
        has_emojis = False
        
        for cell in markdown_cells:
            if re.search(r'^#+\s', cell.source, re.MULTILINE):
                has_headers = True
            if re.search(r'[🎯🟢🟡🔴⚡🧠🚀]', cell.source):
                has_emojis = True
        
        if not has_headers:
            suggestions.append("Use markdown headers for clear visual hierarchy")
        if not has_emojis:
            suggestions.append("Consider using emojis for visual appeal and organization")
        
        return ValidationResult(len(errors) == 0, errors, warnings, suggestions)
    
    def _check_code_quality(self, nb: nbformat.NotebookNode) -> ValidationResult:
        """Check code quality and best practices."""
        errors = []
        warnings = []
        suggestions = []
        
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                code = cell.source
                
                # Check for TODO comments
                if 'TODO' not in code:
                    warnings.append(f"Code cell {i+1} should include TODO comments for student guidance")
                
                # Check for helpful variable names
                if re.search(r'\b[a-z]\b\s*=', code):  # Single letter variables
                    suggestions.append(f"Code cell {i+1}: Consider using descriptive variable names")
                
                # Check for print statements for feedback
                if len(code.strip()) > 50 and 'print(' not in code:
                    suggestions.append(f"Code cell {i+1}: Consider adding print statements for immediate feedback")
        
        return ValidationResult(len(errors) == 0, errors, warnings, suggestions)
    
    def validate_solution(self, solution_path: Path) -> ValidationResult:
        """Validate a solution markdown file."""
        try:
            with open(solution_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return ValidationResult(False, [f"Failed to read solution file: {e}"], [], [])
        
        errors = []
        warnings = []
        suggestions = []
        
        # Check required sections
        required_sections = ['# Solutions', '## Exercise', '### Solution', '### Key Concepts']
        for section in required_sections:
            if section not in content:
                errors.append(f"Solution must include section: {section}")
        
        # Check for code blocks
        code_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        if not code_blocks:
            errors.append("Solution must include code examples in python code blocks")
        
        # Check for explanations
        if '### Alternative Approaches' not in content:
            suggestions.append("Consider including alternative solution approaches")
        
        if '### Common Mistakes' not in content:
            suggestions.append("Consider documenting common mistakes students make")
        
        return ValidationResult(len(errors) == 0, errors, warnings, suggestions)
    
    def generate_report(self, results: Dict[str, ValidationResult]) -> str:
        """Generate a validation report."""
        report = ["# Content Validation Report\n"]
        
        total_files = len(results)
        valid_files = sum(1 for r in results.values() if r.is_valid)
        
        report.append(f"**Summary**: {valid_files}/{total_files} files passed validation\n")
        
        for file_path, result in results.items():
            status = "✅ PASS" if result.is_valid else "❌ FAIL"
            report.append(f"## {file_path} - {status}\n")
            
            if result.errors:
                report.append("### Errors")
                for error in result.errors:
                    report.append(f"- ❌ {error}")
                report.append("")
            
            if result.warnings:
                report.append("### Warnings")
                for warning in result.warnings:
                    report.append(f"- ⚠️ {warning}")
                report.append("")
            
            if result.suggestions:
                report.append("### Suggestions")
                for suggestion in result.suggestions:
                    report.append(f"- 💡 {suggestion}")
                report.append("")
        
        return "\n".join(report)


def main():
    """Main validation function."""
    validator = ContentValidator()
    
    # Find all notebooks and solutions
    notebooks = list(Path('.').glob('*.ipynb'))
    solutions = list(Path('solutions/').glob('*.md'))
    
    results = {}
    
    # Validate notebooks
    for notebook in notebooks:
        if not notebook.name.startswith('.'):  # Skip hidden files
            results[str(notebook)] = validator.validate_notebook(notebook)
    
    # Validate solutions
    for solution in solutions:
        results[str(solution)] = validator.validate_solution(solution)
    
    # Generate and save report
    report = validator.generate_report(results)
    with open('validation_report.md', 'w') as f:
        f.write(report)
    
    print("Validation complete! Check validation_report.md for results.")
    
    # Return exit code based on validation results
    if all(result.is_valid for result in results.values()):
        print("All content passed validation! 🎉")
        return 0
    else:
        print("Some content failed validation. Check the report for details.")
        return 1


if __name__ == "__main__":
    exit(main())