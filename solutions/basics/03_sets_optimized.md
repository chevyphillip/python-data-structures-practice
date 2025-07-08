# Optimized Solutions: Sets Basics

## Exercise 1: Email List Cleanup

### 🟢 Basic Approach (Learning Fundamentals)

```python
newsletter_list = ["alice@email.com", "bob@email.com", "charlie@email.com",
                   "alice@email.com", "diana@email.com", "bob@email.com"]

promotion_list = ["bob@email.com", "eve@email.com", "charlie@email.com",
                  "frank@email.com", "alice@email.com"]

# Manual duplicate removal - educational
unique_newsletter = []
for email in newsletter_list:
    if email not in unique_newsletter:
        unique_newsletter.append(email)

unique_promotion = []
for email in promotion_list:
    if email not in unique_promotion:
        unique_promotion.append(email)

# Convert to sets for operations
newsletter_set = set(unique_newsletter)
promotion_set = set(unique_promotion)

# Manual set operations
common_emails = []
for email in newsletter_set:
    if email in promotion_set:
        common_emails.append(email)

newsletter_only = []
for email in newsletter_set:
    if email not in promotion_set:
        newsletter_only.append(email)

promotion_only = []
for email in promotion_set:
    if email not in newsletter_set:
        promotion_only.append(email)

# Count unique emails
all_unique = set(unique_newsletter + unique_promotion)
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Direct conversion to sets - eliminates duplicates automatically
newsletter_set = set(newsletter_list)
promotion_set = set(promotion_list)

# Using set operations - clean and efficient
common_emails = newsletter_set & promotion_set  # Intersection
newsletter_only = newsletter_set - promotion_set  # Difference
promotion_only = promotion_set - newsletter_set  # Difference
all_unique = newsletter_set | promotion_set  # Union

# Convert back to lists if needed
common_emails = list(common_emails)
newsletter_only = list(newsletter_only)
promotion_only = list(promotion_only)

# Alternative: Using set methods (more explicit)
common_emails = list(newsletter_set.intersection(promotion_set))
newsletter_only = list(newsletter_set.difference(promotion_set))
promotion_only = list(promotion_set.difference(newsletter_set))
all_unique = newsletter_set.union(promotion_set)
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from typing import Set, List, Dict, Tuple
from collections import defaultdict

class EmailListManager:
    """Professional email list management with analytics."""

    def __init__(self):
        self.lists: Dict[str, Set[str]] = {}

    def add_list(self, name: str, emails: List[str]) -> None:
        """Add email list with automatic deduplication."""
        self.lists[name] = set(email.lower().strip() for email in emails)

    def get_intersection(self, *list_names: str) -> Set[str]:
        """Get emails common to all specified lists."""
        if not list_names:
            return set()

        result = self.lists[list_names[0]]
        for name in list_names[1:]:
            result &= self.lists[name]
        return result

    def get_union(self, *list_names: str) -> Set[str]:
        """Get all unique emails across specified lists."""
        result = set()
        for name in list_names:
            result |= self.lists[name]
        return result

    def get_exclusive(self, target_list: str, *exclude_lists: str) -> Set[str]:
        """Get emails exclusive to target list."""
        target = self.lists[target_list]
        for exclude in exclude_lists:
            target -= self.lists[exclude]
        return target

    def analyze_overlap(self) -> Dict[str, Dict]:
        """Comprehensive overlap analysis between all lists."""
        analysis = {}
        list_names = list(self.lists.keys())

        for i, name1 in enumerate(list_names):
            analysis[name1] = {
                'size': len(self.lists[name1]),
                'overlaps': {}
            }

            for name2 in list_names[i+1:]:
                overlap = self.lists[name1] & self.lists[name2]
                overlap_pct = len(overlap) / len(self.lists[name1]) * 100

                analysis[name1]['overlaps'][name2] = {
                    'count': len(overlap),
                    'percentage': overlap_pct,
                    'emails': overlap
                }

        return analysis

    def get_segmentation(self) -> Dict[str, Set[str]]:
        """Advanced segmentation: categorize emails by list membership."""
        all_emails = self.get_union(*self.lists.keys())
        segmentation = defaultdict(set)

        for email in all_emails:
            # Create membership signature
            membership = tuple(
                name for name, email_set in self.lists.items()
                if email in email_set
            )
            segmentation[membership].add(email)

        return dict(segmentation)

# Usage
manager = EmailListManager()
manager.add_list("newsletter", newsletter_list)
manager.add_list("promotion", promotion_list)

# Get results
common_emails = manager.get_intersection("newsletter", "promotion")
newsletter_only = manager.get_exclusive("newsletter", "promotion")
promotion_only = manager.get_exclusive("promotion", "newsletter")
all_unique = manager.get_union("newsletter", "promotion")

# Advanced analytics
overlap_analysis = manager.analyze_overlap()
segmentation = manager.get_segmentation()
```

### 🎯 Key Takeaways

- **Basic**: Manual loops teach set concept fundamentals
- **Optimized**: Set operators (`&`, `|`, `-`) are concise and efficient
- **Advanced**: Classes with comprehensive analytics provide professional solutions
- **Performance**: Set operations are O(1) average case, much faster than list operations
- **Memory**: Sets automatically handle deduplication

### 📊 Performance Comparison

- Manual duplicate removal: O(n²) time complexity
- Set conversion: O(n) time complexity
- Set operations: O(min(len(s1), len(s2))) for intersection
- List membership testing: O(n) per operation
- Set membership testing: O(1) average case

---

## Exercise 2: Course Prerequisites

### 🟢 Basic Approach (Learning Fundamentals)

```python
ai_course_prereqs = {"Python", "Math", "Statistics", "Linear Algebra"}
web_dev_prereqs = {"HTML", "CSS", "JavaScript", "Python"}

alice_courses = {"Python", "Math", "Statistics", "HTML", "CSS"}
bob_courses = {"Python", "Math", "Statistics", "Linear Algebra", "JavaScript"}
charlie_courses = {"HTML", "CSS", "JavaScript", "Python", "React"}

# Manual prerequisite checking
alice_can_take_ai = True
for prereq in ai_course_prereqs:
    if prereq not in alice_courses:
        alice_can_take_ai = False
        break

# Find missing prerequisites manually
alice_missing_ai = []
for prereq in ai_course_prereqs:
    if prereq not in alice_courses:
        alice_missing_ai.append(prereq)

# Check all students for web development
students = {
    "Alice": alice_courses,
    "Bob": bob_courses,
    "Charlie": charlie_courses
}

web_eligible = []
for student, courses in students.items():
    can_take = True
    for prereq in web_dev_prereqs:
        if prereq not in courses:
            can_take = False
            break
    if can_take:
        web_eligible.append(student)

# Find super students manually
all_prereqs = set()
for prereq in ai_course_prereqs:
    all_prereqs.add(prereq)
for prereq in web_dev_prereqs:
    all_prereqs.add(prereq)

super_students = []
for student, courses in students.items():
    has_all = True
    for prereq in all_prereqs:
        if prereq not in courses:
            has_all = False
            break
    if has_all:
        super_students.append(student)
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Using set methods - clean and readable
alice_can_take_ai = ai_course_prereqs.issubset(alice_courses)
# Alternative: alice_courses.issuperset(ai_course_prereqs)

# Find missing prerequisites using set difference
alice_missing_ai = ai_course_prereqs - alice_courses

# Check all students using comprehension
web_eligible = [
    student for student, courses in students.items()
    if web_dev_prereqs.issubset(courses)
]

# Find super students using union and subset
all_prereqs = ai_course_prereqs | web_dev_prereqs
super_students = [
    student for student, courses in students.items()
    if all_prereqs.issubset(courses)
]

# Alternative: More explicit with set methods
web_eligible = [
    student for student, courses in students.items()
    if courses.issuperset(web_dev_prereqs)
]

# Check multiple prerequisites at once
def check_eligibility(student_courses, *required_sets):
    """Check if student meets all requirement sets."""
    return all(reqs.issubset(student_courses) for reqs in required_sets)

# Usage
alice_can_take_both = check_eligibility(alice_courses, ai_course_prereqs, web_dev_prereqs)
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from typing import Dict, Set, List, Tuple
from collections import defaultdict
from enum import Enum

class PrerequisiteStatus(Enum):
    ELIGIBLE = "eligible"
    MISSING_PREREQS = "missing_prerequisites"
    OVERQUALIFIED = "overqualified"

class CourseManager:
    """Advanced course prerequisite management system."""

    def __init__(self):
        self.courses: Dict[str, Set[str]] = {}
        self.students: Dict[str, Set[str]] = {}
        self.prerequisite_chains: Dict[str, Set[str]] = {}

    def add_course(self, name: str, prerequisites: Set[str]) -> None:
        """Add course with prerequisites."""
        self.courses[name] = prerequisites.copy()

    def add_student(self, name: str, completed_courses: Set[str]) -> None:
        """Add student with completed courses."""
        self.students[name] = completed_courses.copy()

    def check_eligibility(self, student: str, course: str) -> Tuple[PrerequisiteStatus, Set[str]]:
        """Check student eligibility with detailed status."""
        if student not in self.students or course not in self.courses:
            raise ValueError("Student or course not found")

        student_courses = self.students[student]
        required = self.courses[course]
        missing = required - student_courses

        if not missing:
            # Check if overqualified (has more than needed)
            extra = student_courses - required
            if len(extra) > len(required):
                return PrerequisiteStatus.OVERQUALIFIED, extra
            return PrerequisiteStatus.ELIGIBLE, set()

        return PrerequisiteStatus.MISSING_PREREQS, missing

    def get_eligible_students(self, course: str) -> List[str]:
        """Get all students eligible for a course."""
        if course not in self.courses:
            return []

        required = self.courses[course]
        return [
            student for student, courses in self.students.items()
            if required.issubset(courses)
        ]

    def get_student_opportunities(self, student: str) -> Dict[str, PrerequisiteStatus]:
        """Get all courses a student can take with status."""
        if student not in self.students:
            return {}

        opportunities = {}
        for course in self.courses:
            status, _ = self.check_eligibility(student, course)
            opportunities[course] = status

        return opportunities

    def recommend_next_courses(self, student: str) -> List[Tuple[str, Set[str]]]:
        """Recommend courses student is closest to qualifying for."""
        if student not in self.students:
            return []

        recommendations = []
        student_courses = self.students[student]

        for course, prereqs in self.courses.items():
            missing = prereqs - student_courses
            if 0 < len(missing) <= 2:  # Close to qualifying
                recommendations.append((course, missing))

        # Sort by fewest missing prerequisites
        return sorted(recommendations, key=lambda x: len(x[1]))

    def analyze_course_difficulty(self) -> Dict[str, Dict]:
        """Analyze course accessibility based on prerequisites."""
        analysis = {}

        for course, prereqs in self.courses.items():
            eligible_count = len(self.get_eligible_students(course))
            total_students = len(self.students)

            analysis[course] = {
                'prerequisite_count': len(prereqs),
                'eligible_students': eligible_count,
                'accessibility_rate': eligible_count / total_students if total_students > 0 else 0,
                'prerequisites': prereqs
            }

        return analysis

# Usage
manager = CourseManager()
manager.add_course("AI Course", ai_course_prereqs)
manager.add_course("Web Development", web_dev_prereqs)

manager.add_student("Alice", alice_courses)
manager.add_student("Bob", bob_courses)
manager.add_student("Charlie", charlie_courses)

# Check specific eligibility
alice_ai_status, alice_missing = manager.check_eligibility("Alice", "AI Course")
web_eligible = manager.get_eligible_students("Web Development")

# Get comprehensive analysis
alice_opportunities = manager.get_student_opportunities("Alice")
recommendations = manager.recommend_next_courses("Alice")
course_analysis = manager.analyze_course_difficulty()
```

### 🎯 Key Takeaways

- **Basic**: Manual loops teach prerequisite logic
- **Optimized**: `issubset()` and `issuperset()` are clear and efficient
- **Advanced**: Comprehensive systems handle complex prerequisite relationships
- **Set operations**: Perfect for prerequisite checking (subset relationships)
- **Scalability**: Set-based solutions scale well with large course catalogs

---

## Exercise 3: Text Analysis with Sets

### 🟢 Basic Approach (Learning Fundamentals)

```python
doc1 = "machine learning artificial intelligence python programming"
doc2 = "python programming data science machine learning algorithms"

# Manual word extraction and deduplication
words1 = []
for word in doc1.split():
    if word not in words1:
        words1.append(word)

words2 = []
for word in doc2.split():
    if word not in words2:
        words2.append(word)

# Manual set operations
common_words = []
for word in words1:
    if word in words2:
        common_words.append(word)

unique_to_doc1 = []
for word in words1:
    if word not in words2:
        unique_to_doc1.append(word)

unique_to_doc2 = []
for word in words2:
    if word not in words1:
        unique_to_doc2.append(word)

# Manual similarity calculation
all_unique_words = []
for word in words1:
    if word not in all_unique_words:
        all_unique_words.append(word)
for word in words2:
    if word not in all_unique_words:
        all_unique_words.append(word)

similarity = (len(common_words) / len(all_unique_words)) * 100
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Direct set conversion - automatic deduplication
words1 = set(doc1.split())
words2 = set(doc2.split())

# Clean set operations
common_words = words1 & words2
unique_to_doc1 = words1 - words2
unique_to_doc2 = words2 - words1
total_unique = words1 | words2

# Jaccard similarity coefficient
similarity = (len(common_words) / len(total_unique)) * 100

# Alternative similarity metrics
def calculate_similarities(set1, set2):
    """Calculate multiple similarity metrics."""
    intersection = set1 & set2
    union = set1 | set2

    return {
        'jaccard': len(intersection) / len(union) if union else 0,
        'dice': (2 * len(intersection)) / (len(set1) + len(set2)) if (set1 or set2) else 0,
        'overlap': len(intersection) / min(len(set1), len(set2)) if (set1 and set2) else 0,
        'cosine': len(intersection) / (len(set1) * len(set2))**0.5 if (set1 and set2) else 0
    }

similarities = calculate_similarities(words1, words2)
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from typing import Set, List, Dict, Tuple
import re
from collections import Counter
import math

class TextAnalyzer:
    """Advanced text analysis using set operations and NLP techniques."""

    def __init__(self, preprocessing: bool = True):
        self.preprocessing = preprocessing
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being'
        }

    def preprocess_text(self, text: str) -> List[str]:
        """Advanced text preprocessing."""
        if not self.preprocessing:
            return text.split()

        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', '', text.lower())
        words = text.split()

        # Remove stopwords and short words
        return [word for word in words if word not in self.stopwords and len(word) > 2]

    def analyze_documents(self, *documents: str) -> Dict:
        """Comprehensive multi-document analysis."""
        doc_sets = [set(self.preprocess_text(doc)) for doc in documents]

        # Basic set operations
        intersection = set.intersection(*doc_sets) if doc_sets else set()
        union = set.union(*doc_sets) if doc_sets else set()

        # Pairwise similarities
        similarities = {}
        for i, set1 in enumerate(doc_sets):
            for j, set2 in enumerate(doc_sets[i+1:], i+1):
                similarities[f'doc{i+1}_doc{j+1}'] = self._calculate_similarity_metrics(set1, set2)

        # Document uniqueness
        unique_words = {}
        for i, doc_set in enumerate(doc_sets):
            others = set.union(*(doc_sets[:i] + doc_sets[i+1:])) if len(doc_sets) > 1 else set()
            unique_words[f'doc{i+1}'] = doc_set - others

        return {
            'document_count': len(documents),
            'total_unique_words': len(union),
            'common_words': intersection,
            'common_word_count': len(intersection),
            'pairwise_similarities': similarities,
            'unique_to_each': unique_words,
            'vocabulary_overlap': len(intersection) / len(union) if union else 0
        }

    def _calculate_similarity_metrics(self, set1: Set[str], set2: Set[str]) -> Dict[str, float]:
        """Calculate comprehensive similarity metrics."""
        intersection = set1 & set2
        union = set1 | set2

        metrics = {
            'jaccard': len(intersection) / len(union) if union else 0,
            'dice': (2 * len(intersection)) / (len(set1) + len(set2)) if (set1 or set2) else 0,
            'overlap': len(intersection) / min(len(set1), len(set2)) if (set1 and set2) else 0,
            'cosine': len(intersection) / math.sqrt(len(set1) * len(set2)) if (set1 and set2) else 0
        }

        return metrics

    def find_semantic_clusters(self, documents: List[str], threshold: float = 0.3) -> List[List[int]]:
        """Group documents by similarity threshold."""
        doc_sets = [set(self.preprocess_text(doc)) for doc in documents]
        clusters = []
        used = set()

        for i, set1 in enumerate(doc_sets):
            if i in used:
                continue

            cluster = [i]
            used.add(i)

            for j, set2 in enumerate(doc_sets[i+1:], i+1):
                if j in used:
                    continue

                similarity = self._calculate_similarity_metrics(set1, set2)['jaccard']
                if similarity >= threshold:
                    cluster.append(j)
                    used.add(j)

            clusters.append(cluster)

        return clusters

    def extract_key_terms(self, documents: List[str], top_n: int = 10) -> Dict[str, List[Tuple[str, float]]]:
        """Extract key terms using TF-IDF-like scoring with sets."""
        doc_sets = [set(self.preprocess_text(doc)) for doc in documents]
        all_words = set.union(*doc_sets) if doc_sets else set()

        # Calculate document frequency for each word
        doc_freq = {}
        for word in all_words:
            doc_freq[word] = sum(1 for doc_set in doc_sets if word in doc_set)

        # Calculate importance score (inverse document frequency)
        total_docs = len(documents)
        key_terms = {}

        for i, doc_set in enumerate(doc_sets):
            scores = []
            for word in doc_set:
                # Simple IDF: log(total_docs / doc_frequency)
                idf = math.log(total_docs / doc_freq[word]) if doc_freq[word] > 0 else 0
                scores.append((word, idf))

            # Sort by score and take top N
            scores.sort(key=lambda x: x[1], reverse=True)
            key_terms[f'doc{i+1}'] = scores[:top_n]

        return key_terms

# Usage examples
analyzer = TextAnalyzer(preprocessing=True)

# Multi-document analysis
docs = [
    "machine learning artificial intelligence python programming",
    "python programming data science machine learning algorithms",
    "artificial intelligence deep learning neural networks"
]

analysis = analyzer.analyze_documents(*docs)
clusters = analyzer.find_semantic_clusters(docs, threshold=0.2)
key_terms = analyzer.extract_key_terms(docs, top_n=5)

# Simple two-document comparison
doc1 = "machine learning artificial intelligence python programming"
doc2 = "python programming data science machine learning algorithms"

simple_analysis = analyzer.analyze_documents(doc1, doc2)
similarity_score = simple_analysis['pairwise_similarities']['doc1_doc2']['jaccard']
```

### 🎯 Key Takeaways

- **Basic**: Manual operations teach set fundamentals
- **Optimized**: Set operators provide clean, efficient text analysis
- **Advanced**: Professional NLP techniques with set-based optimizations
- **Similarity metrics**: Multiple approaches for different use cases
- **Scalability**: Set operations scale well for large document collections

### 📊 Performance & Use Cases

- **Jaccard similarity**: Best for general document similarity
- **Dice coefficient**: Emphasizes common elements more than unique ones
- **Overlap coefficient**: Good when documents have very different sizes
- **Cosine similarity**: Traditional choice for text analysis
- **Set operations**: O(min(len(s1), len(s2))) for intersection, very efficient
