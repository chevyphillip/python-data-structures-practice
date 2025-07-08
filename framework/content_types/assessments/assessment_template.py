#!/usr/bin/env python3
"""
Assessment Template for Python Data Structures Learning Framework

This template provides quiz-style assessment with auto-grading functionality.
"""

import json
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Question:
    """A single assessment question."""
    id: str
    question: str
    question_type: str  # 'multiple_choice', 'code_completion', 'short_answer'
    options: List[str] = None  # For multiple choice
    correct_answer: Any = None
    explanation: str = ""
    points: int = 1
    difficulty: str = "intermediate"  # beginner, intermediate, advanced


@dataclass
class AssessmentResult:
    """Results from taking an assessment."""
    student_answers: Dict[str, Any]
    score: int
    total_points: int
    percentage: float
    feedback: List[str]
    time_taken: float


class Assessment:
    """Interactive assessment with auto-grading."""
    
    def __init__(self, title: str, description: str, time_limit: int = 30):
        self.title = title
        self.description = description
        self.time_limit = time_limit  # minutes
        self.questions: List[Question] = []
        self.start_time = None
    
    def add_question(self, question: Question):
        """Add a question to the assessment."""
        self.questions.append(question)
    
    def take_assessment(self) -> AssessmentResult:
        """Interactive assessment taking."""
        print(f"\n{'='*50}")
        print(f"📋 {self.title}")
        print(f"{'='*50}")
        print(f"{self.description}")
        print(f"⏱️ Time limit: {self.time_limit} minutes")
        print(f"📝 Questions: {len(self.questions)}")
        print(f"{'='*50}\n")
        
        input("Press Enter to start the assessment...")
        self.start_time = datetime.now()
        
        student_answers = {}
        
        for i, question in enumerate(self.questions, 1):
            print(f"\n--- Question {i}/{len(self.questions)} ---")
            answer = self._ask_question(question)
            student_answers[question.id] = answer
        
        end_time = datetime.now()
        time_taken = (end_time - self.start_time).total_seconds() / 60
        
        return self._grade_assessment(student_answers, time_taken)
    
    def _ask_question(self, question: Question) -> Any:
        """Present a single question and get student answer."""
        print(f"\n🎯 {question.question}")
        
        if question.question_type == 'multiple_choice':
            return self._ask_multiple_choice(question)
        elif question.question_type == 'code_completion':
            return self._ask_code_completion(question)
        elif question.question_type == 'short_answer':
            return self._ask_short_answer(question)
        else:
            return input("Answer: ").strip()
    
    def _ask_multiple_choice(self, question: Question) -> str:
        """Handle multiple choice questions."""
        for i, option in enumerate(question.options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = input("\nSelect option (1-{}): ".format(len(question.options)))
                choice_num = int(choice)
                if 1 <= choice_num <= len(question.options):
                    return question.options[choice_num - 1]
                else:
                    print("Please select a valid option number.")
            except ValueError:
                print("Please enter a number.")
    
    def _ask_code_completion(self, question: Question) -> str:
        """Handle code completion questions."""
        print("\n💻 Complete the following code:")
        print("Type your answer on multiple lines. Enter 'DONE' on a new line when finished.")
        
        lines = []
        while True:
            line = input(">>> " if not lines else "... ")
            if line.strip() == 'DONE':
                break
            lines.append(line)
        
        return '\n'.join(lines)
    
    def _ask_short_answer(self, question: Question) -> str:
        """Handle short answer questions."""
        return input("Answer: ").strip()
    
    def _grade_assessment(self, student_answers: Dict[str, Any], time_taken: float) -> AssessmentResult:
        """Grade the assessment and provide feedback."""
        score = 0
        total_points = sum(q.points for q in self.questions)
        feedback = []
        
        for question in self.questions:
            student_answer = student_answers.get(question.id, "")
            is_correct = self._check_answer(question, student_answer)
            
            if is_correct:
                score += question.points
                feedback.append(f"✅ Question {question.id}: Correct! {question.explanation}")
            else:
                feedback.append(f"❌ Question {question.id}: Incorrect. {question.explanation}")
        
        percentage = (score / total_points) * 100 if total_points > 0 else 0
        
        return AssessmentResult(
            student_answers=student_answers,
            score=score,
            total_points=total_points,
            percentage=percentage,
            feedback=feedback,
            time_taken=time_taken
        )
    
    def _check_answer(self, question: Question, student_answer: Any) -> bool:
        """Check if student answer is correct."""
        if question.question_type == 'multiple_choice':
            return student_answer == question.correct_answer
        elif question.question_type == 'code_completion':
            return self._check_code_answer(question.correct_answer, student_answer)
        elif question.question_type == 'short_answer':
            # Case-insensitive comparison for short answers
            return student_answer.lower().strip() == question.correct_answer.lower().strip()
        else:
            return str(student_answer).strip() == str(question.correct_answer).strip()
    
    def _check_code_answer(self, expected: str, student_code: str) -> bool:
        """Check code completion answers (basic implementation)."""
        # This is a simplified check - in a real implementation, you might
        # want to execute the code and check output or use AST comparison
        expected_normalized = expected.replace(' ', '').replace('\n', '')
        student_normalized = student_code.replace(' ', '').replace('\n', '')
        return expected_normalized == student_normalized
    
    def display_results(self, result: AssessmentResult):
        """Display assessment results."""
        print(f"\n{'='*50}")
        print(f"📊 Assessment Results")
        print(f"{'='*50}")
        print(f"Score: {result.score}/{result.total_points} ({result.percentage:.1f}%)")
        print(f"Time taken: {result.time_taken:.1f} minutes")
        
        # Performance level
        if result.percentage >= 90:
            print("🏆 Excellent work!")
        elif result.percentage >= 80:
            print("🎉 Great job!")
        elif result.percentage >= 70:
            print("👍 Good effort!")
        else:
            print("📚 Keep practicing!")
        
        print(f"\n--- Detailed Feedback ---")
        for feedback_item in result.feedback:
            print(feedback_item)
        
        print(f"{'='*50}\n")


# Example Usage and Template
def create_lists_assessment() -> Assessment:
    """Create a sample assessment for lists."""
    assessment = Assessment(
        title="Lists Fundamentals Assessment",
        description="Test your knowledge of Python lists with 5 questions covering basic operations.",
        time_limit=15
    )
    
    # Question 1: Multiple Choice
    assessment.add_question(Question(
        id="q1",
        question="What is the output of `my_list = [1, 2, 3]; print(my_list[1])`?",
        question_type="multiple_choice",
        options=["1", "2", "3", "IndexError"],
        correct_answer="2",
        explanation="List indexing starts at 0, so index 1 refers to the second element.",
        points=1,
        difficulty="beginner"
    ))
    
    # Question 2: Code Completion
    assessment.add_question(Question(
        id="q2",
        question="Complete this code to add 'apple' to the end of the list:\nfruits = ['banana', 'orange']\n# Your code here",
        question_type="code_completion",
        correct_answer="fruits.append('apple')",
        explanation="The append() method adds an element to the end of a list.",
        points=2,
        difficulty="beginner"
    ))
    
    # Question 3: Short Answer
    assessment.add_question(Question(
        id="q3",
        question="What method would you use to remove the last element from a list?",
        question_type="short_answer",
        correct_answer="pop",
        explanation="The pop() method removes and returns the last element from a list.",
        points=1,
        difficulty="beginner"
    ))
    
    return assessment


if __name__ == "__main__":
    # Run the sample assessment
    assessment = create_lists_assessment()
    result = assessment.take_assessment()
    assessment.display_results(result)