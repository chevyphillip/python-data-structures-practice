#!/usr/bin/env python3
"""
Exercise Generator for Python Data Structures Learning Framework

This tool generates new exercises from templates with customizable parameters.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import argparse


class ExerciseGenerator:
    """Generates new exercises from templates."""
    
    def __init__(self, templates_dir: Path = Path("framework/templates")):
        self.templates_dir = templates_dir
        self.exercise_template = templates_dir / "exercise_template.ipynb"
        self.solution_template = templates_dir / "solution_template.md" 
        self.data_template = templates_dir / "data_template.json"
    
    def generate_exercise(self, config: Dict[str, Any], output_dir: Path = Path(".")):
        """Generate a new exercise from configuration."""
        
        # Validate configuration
        self._validate_config(config)
        
        # Generate files
        exercise_file = self._generate_notebook(config, output_dir)
        solution_file = self._generate_solution(config, output_dir)
        data_file = self._generate_data(config, output_dir) if config.get('include_data') else None
        
        # Update index files
        self._update_documentation(config, exercise_file)
        
        return {
            'exercise': exercise_file,
            'solution': solution_file,
            'data': data_file
        }
    
    def _validate_config(self, config: Dict[str, Any]):
        """Validate that configuration has required fields."""
        required_fields = [
            'topic_name', 'difficulty_level', 'learning_objective',
            'estimated_time', 'data_structures_list'
        ]
        
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required configuration fields: {missing_fields}")
        
        # Validate difficulty level
        valid_difficulties = ['beginner', 'intermediate', 'advanced']
        if config['difficulty_level'].lower() not in valid_difficulties:
            raise ValueError(f"Difficulty must be one of: {valid_difficulties}")
    
    def _generate_notebook(self, config: Dict[str, Any], output_dir: Path) -> Path:
        """Generate exercise notebook from template."""
        
        # Read template
        with open(self.exercise_template, 'r') as f:
            template_content = f.read()
        
        # Prepare substitution variables
        substitutions = self._prepare_substitutions(config)
        
        # Perform substitutions
        content = self._substitute_variables(template_content, substitutions)
        
        # Generate filename
        number = self._get_next_exercise_number(output_dir)
        topic_slug = self._slugify(config['topic_name'])
        level_slug = config['difficulty_level'].lower()
        filename = f"{number:02d}_{topic_slug}_{level_slug}.ipynb"
        
        # Write file
        output_file = output_dir / filename
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"Generated exercise: {output_file}")
        return output_file
    
    def _generate_solution(self, config: Dict[str, Any], output_dir: Path) -> Path:
        """Generate solution file from template."""
        
        # Read template
        with open(self.solution_template, 'r') as f:
            template_content = f.read()
        
        # Prepare substitution variables
        substitutions = self._prepare_substitutions(config)
        
        # Perform substitutions
        content = self._substitute_variables(template_content, substitutions)
        
        # Generate filename
        number = self._get_next_exercise_number(output_dir)
        topic_slug = self._slugify(config['topic_name'])
        filename = f"{number:02d}_{topic_slug}_solutions.md"
        
        # Write file
        solutions_dir = output_dir / "solutions"
        solutions_dir.mkdir(exist_ok=True)
        output_file = solutions_dir / filename
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"Generated solution: {output_file}")
        return output_file
    
    def _generate_data(self, config: Dict[str, Any], output_dir: Path) -> Path:
        """Generate data file from template if needed."""
        
        if not config.get('sample_data'):
            return None
        
        # Read template
        with open(self.data_template, 'r') as f:
            template_content = f.read()
        
        # Prepare substitution variables
        substitutions = self._prepare_substitutions(config)
        substitutions['CREATION_DATE'] = datetime.now().isoformat()
        
        # Perform substitutions
        content = self._substitute_variables(template_content, substitutions)
        
        # Generate filename
        topic_slug = self._slugify(config['topic_name'])
        filename = f"{topic_slug}_data.json"
        
        # Write file
        data_dir = output_dir / "data"
        data_dir.mkdir(exist_ok=True)
        output_file = data_dir / filename
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"Generated data: {output_file}")
        return output_file
    
    def _prepare_substitutions(self, config: Dict[str, Any]) -> Dict[str, str]:
        """Prepare variable substitutions from configuration."""
        
        # Difficulty level mappings
        difficulty_emojis = {
            'beginner': '🟢',
            'intermediate': '🟡',
            'advanced': '🔴'
        }
        
        difficulty_texts = {
            'beginner': 'Beginner',
            'intermediate': 'Intermediate', 
            'advanced': 'Advanced'
        }
        
        # Base substitutions
        substitutions = {
            'TOPIC_NAME': config['topic_name'],
            'DIFFICULTY_LEVEL': config['difficulty_level'].title(),
            'DIFFICULTY_EMOJI': difficulty_emojis.get(config['difficulty_level'].lower(), '🟢'),
            'DIFFICULTY_TEXT': difficulty_texts.get(config['difficulty_level'].lower(), 'Beginner'),
            'LEARNING_OBJECTIVE': config['learning_objective'],
            'ESTIMATED_TIME': str(config['estimated_time']),
            'DATA_STRUCTURES_LIST': ', '.join(config['data_structures_list']),
        }
        
        # Add exercise-specific substitutions
        for i in range(1, 4):  # Support up to 3 exercises
            exercise_key = f'exercise_{i}'
            if exercise_key in config:
                exercise_config = config[exercise_key]
                substitutions.update({
                    f'EXERCISE_{i}_TITLE': exercise_config.get('title', f'Exercise {i}'),
                    f'EXERCISE_{i}_DESCRIPTION': exercise_config.get('description', ''),
                    f'SAMPLE_DATA_{i}': exercise_config.get('sample_data', ''),
                    f'HELPFUL_HINT_{i}': exercise_config.get('hint', ''),
                })
                
                # Add task substitutions
                tasks = exercise_config.get('tasks', [])
                for j, task in enumerate(tasks[:3], 1):  # Support up to 3 tasks per exercise
                    substitutions[f'TASK_{(i-1)*3 + j}'] = task
        
        # Add challenge substitutions
        if 'challenge' in config:
            challenge_config = config['challenge']
            substitutions.update({
                'CHALLENGE_DESCRIPTION': challenge_config.get('description', ''),
                'CHALLENGE_DATA': challenge_config.get('data', ''),
                'CHALLENGE_HINT': challenge_config.get('hint', ''),
                'CHALLENGE_FOCUS': challenge_config.get('focus', 'efficiency and readability'),
            })
        
        # Add any custom substitutions
        substitutions.update(config.get('custom_substitutions', {}))
        
        return substitutions
    
    def _substitute_variables(self, content: str, substitutions: Dict[str, str]) -> str:
        """Perform variable substitution in content."""
        
        for key, value in substitutions.items():
            # Handle both {KEY} and {KEY} patterns
            content = content.replace(f'{{{key}}}', str(value))
        
        # Clean up any remaining template variables
        content = re.sub(r'\{[A-Z_]+\}', '[TODO: Configure this value]', content)
        
        return content
    
    def _get_next_exercise_number(self, output_dir: Path) -> int:
        """Get the next available exercise number."""
        
        existing_files = list(output_dir.glob('[0-9][0-9]_*.ipynb'))
        if not existing_files:
            return 1
        
        # Extract numbers and find the maximum
        numbers = []
        for file in existing_files:
            match = re.match(r'(\d+)_', file.name)
            if match:
                numbers.append(int(match.group(1)))
        
        return max(numbers) + 1 if numbers else 1
    
    def _slugify(self, text: str) -> str:
        """Convert text to a URL-friendly slug."""
        
        # Convert to lowercase and replace spaces with underscores
        slug = text.lower().replace(' ', '_')
        
        # Remove non-alphanumeric characters except underscores
        slug = re.sub(r'[^a-z0-9_]', '', slug)
        
        # Remove multiple consecutive underscores
        slug = re.sub(r'_+', '_', slug)
        
        # Remove leading/trailing underscores
        slug = slug.strip('_')
        
        return slug
    
    def _update_documentation(self, config: Dict[str, Any], exercise_file: Path):
        """Update documentation to include new exercise."""
        
        # Update README.md
        readme_path = Path('README.md')
        if readme_path.exists():
            self._add_to_readme(config, exercise_file, readme_path)
        
        # Update study guide
        study_guide_path = Path('STUDY_GUIDE.md')
        if study_guide_path.exists():
            self._add_to_study_guide(config, exercise_file, study_guide_path)
    
    def _add_to_readme(self, config: Dict[str, Any], exercise_file: Path, readme_path: Path):
        """Add new exercise to README.md."""
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # Find the exercises section
        exercise_pattern = r'(### 📁 Exercises.*?)(\n### |\n## |\Z)'
        match = re.search(exercise_pattern, content, re.DOTALL)
        
        if match:
            exercises_section = match.group(1)
            difficulty_emoji = {'beginner': '🟢', 'intermediate': '🟡', 'advanced': '🔴'}
            emoji = difficulty_emoji.get(config['difficulty_level'].lower(), '🟢')
            
            new_line = f"- `{exercise_file.name}` - {config['topic_name']} ({emoji} {config['difficulty_level'].title()})"
            updated_section = exercises_section + f"\n{new_line}"
            
            content = content.replace(exercises_section, updated_section)
            
            with open(readme_path, 'w') as f:
                f.write(content)
            
            print(f"Updated {readme_path} with new exercise")
    
    def _add_to_study_guide(self, config: Dict[str, Any], exercise_file: Path, study_guide_path: Path):
        """Add new exercise to study guide."""
        # Implementation for updating study guide
        # This would add the exercise to the appropriate week/difficulty section
        pass


def main():
    """Main function for command-line usage."""
    
    parser = argparse.ArgumentParser(description='Generate new exercises from templates')
    parser.add_argument('config_file', help='Path to configuration JSON file')
    parser.add_argument('--output-dir', default='.', help='Output directory for generated files')
    
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config_file, 'r') as f:
        config = json.load(f)
    
    # Generate exercise
    generator = ExerciseGenerator()
    output_dir = Path(args.output_dir)
    
    try:
        files = generator.generate_exercise(config, output_dir)
        print(f"\nSuccessfully generated exercise files:")
        for file_type, file_path in files.items():
            if file_path:
                print(f"  {file_type}: {file_path}")
    
    except Exception as e:
        print(f"Error generating exercise: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())