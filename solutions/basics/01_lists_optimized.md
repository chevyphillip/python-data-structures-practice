# Optimized Solutions: Lists Basics

## Exercise 1: Music Playlist Creation

### 🟢 Basic Approach (Learning Fundamentals)

```python
music_data = ["Blinding Lights", "The Weeknd", "Pop", "One Dance", "Drake", "Pop",
              "Bohemian Rhapsody", "Queen", "Rock", "Shape of You", "Ed Sheeran", "Pop"]

# Extract using slicing - shows understanding of indexing
songs = music_data[::3]     # [0, 3, 6, 9] -> songs
artists = music_data[1::3]  # [1, 4, 7, 10] -> artists
genres = music_data[2::3]   # [2, 5, 8, 11] -> genres
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Using zip with iterator unpacking - more elegant and readable
def chunk_data(data, size):
    """Split data into chunks of specified size."""
    return zip(*[iter(data)] * size)

# Create structured data in one operation
playlist = list(chunk_data(music_data, 3))
songs, artists, genres = zip(*playlist)  # Unpack all at once

# Alternative: Direct unpacking with zip
songs, artists, genres = zip(*[music_data[i:i+3] for i in range(0, len(music_data), 3)])
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from itertools import islice
from typing import Iterator, Tuple, List

def chunk_iterator(data: List[str], size: int) -> Iterator[Tuple[str, ...]]:
    """Memory-efficient chunking using itertools."""
    it = iter(data)
    while chunk := tuple(islice(it, size)):
        if len(chunk) == size:
            yield chunk

# Create structured playlist with named tuples for clarity
from collections import namedtuple
Track = namedtuple('Track', ['song', 'artist', 'genre'])

playlist = [Track(*chunk) for chunk in chunk_iterator(music_data, 3)]
songs = [track.song for track in playlist]
artists = [track.artist for track in playlist]
genres = [track.genre for track in playlist]

# Or using operator.attrgetter for even more efficiency
from operator import attrgetter
songs = list(map(attrgetter('song'), playlist))
```

### 🎯 Key Takeaways

- **Basic**: Slicing teaches indexing fundamentals
- **Optimized**: `zip()` with unpacking is more readable and Pythonic
- **Advanced**: `itertools` provides memory-efficient solutions for large datasets
- **When to use**: Basic for learning, optimized for most code, advanced for performance-critical applications

---

## Exercise 2: List Manipulation

### 🟢 Basic Approach (Learning Fundamentals)

```python
test_scores = [85, 92, 78, 96, 88, 76, 94, 82, 90, 87]

# Individual operations - clear and educational
highest = max(test_scores)
lowest = min(test_scores)
average = sum(test_scores) / len(test_scores)
high_scores = [score for score in test_scores if score > 90]
last_three = test_scores[-3:]
reversed_scores = test_scores[::-1]
```

### 🟡 Optimized Approach (Pythonic Style)

```python
import statistics

# Use statistics module for more robust calculations
highest, lowest = max(test_scores), min(test_scores)
average = statistics.mean(test_scores)  # More precise than manual calculation
median = statistics.median(test_scores)  # Additional insight

# Combine operations using built-in functions
high_scores = list(filter(lambda x: x > 90, test_scores))
# Or using any() for boolean check
has_high_scores = any(score > 90 for score in test_scores)

# Multiple operations in one pass using generator
stats = {
    'count': len(test_scores),
    'sum': sum(test_scores),
    'min': min(test_scores),
    'max': max(test_scores),
    'avg': statistics.mean(test_scores)
}
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from functools import reduce
from operator import add, gt
from itertools import compress

# Functional programming approach
def analyze_scores(scores):
    """Comprehensive score analysis using functional programming."""
    return {
        'total': reduce(add, scores),
        'count': len(scores),
        'average': reduce(add, scores) / len(scores),
        'range': max(scores) - min(scores),
        'high_scores': list(compress(scores, map(lambda x: x > 90, scores))),
        'percentiles': {
            p: statistics.quantiles(scores, n=100)[p-1]
            for p in [25, 50, 75]
        }
    }

result = analyze_scores(test_scores)

# Memory-efficient filtering with generators
high_score_gen = (score for score in test_scores if score > 90)
# Only materialize when needed
high_scores = list(high_score_gen)
```

### 📊 Performance Comparison

- **List comprehension**: ~2x faster than manual loops
- **filter() with lambda**: Similar to comprehension, more functional style
- **Generator expressions**: Memory-efficient for large datasets
- **statistics module**: More accurate for floating-point calculations

---

## Exercise 3: List Comprehensions

### 🟢 Basic Approach (Learning Fundamentals)

```python
# Simple comprehensions - learning the syntax
squares = [n**2 for n in range(1, 11)]
evens = [n for n in range(21) if n % 2 == 0]

words = ["cat", "elephant", "dog", "rhinoceros", "bird", "hippopotamus"]
long_words = [word for word in words if len(word) > 4]

celsius_temps = [0, 10, 20, 30, 37, 100]
fahrenheit_temps = [(c * 9/5) + 32 for c in celsius_temps]
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Using map() for transformations - more functional
squares = list(map(lambda x: x**2, range(1, 11)))
# Or using pow function directly
squares = list(map(pow, range(1, 11), [2]*10))

# Generator expressions for memory efficiency
evens_gen = (n for n in range(21) if n % 2 == 0)
evens = list(evens_gen)  # Materialize only when needed

# Using filter() with built-in functions
long_words = list(filter(lambda w: len(w) > 4, words))

# Temperature conversion with named function for clarity
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

fahrenheit_temps = list(map(celsius_to_fahrenheit, celsius_temps))
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from operator import mul, pow as op_pow
from functools import partial

# Using operator module for better performance
squares = list(map(partial(op_pow, exp=2), range(1, 11)))

# Advanced filtering with multiple conditions
def advanced_word_filter(words, min_length=4, max_length=float('inf')):
    """Filter words by length with configurable bounds."""
    return list(filter(
        lambda w: min_length < len(w) <= max_length,
        words
    ))

long_words = advanced_word_filter(words, min_length=4)

# Temperature conversion with validation
def safe_temp_converter(temps, from_unit='C', to_unit='F'):
    """Convert temperatures with validation."""
    converters = {
        ('C', 'F'): lambda c: (c * 9/5) + 32,
        ('F', 'C'): lambda f: (f - 32) * 5/9,
    }

    converter = converters.get((from_unit, to_unit))
    if not converter:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported")

    return [converter(temp) for temp in temps if isinstance(temp, (int, float))]

fahrenheit_temps = safe_temp_converter(celsius_temps)
```

### 🎯 Key Takeaways

- **Comprehensions**: Most Pythonic for simple transformations
- **map()/filter()**: Better for functional programming style
- **Generators**: Essential for memory efficiency with large datasets
- **operator module**: Performance boost for simple operations

---

## Quick Challenge: Data Type Separation

### 🟢 Basic Approach (Learning Fundamentals)

```python
messy_data = [1, "hello", 3.14, "world", 42, "python", 2.71, "coding"]

# Manual type checking - educational
numbers = []
strings = []

for item in messy_data:
    if isinstance(item, (int, float)):
        numbers.append(item)
    elif isinstance(item, str):
        strings.append(item)

numbers.sort()
strings.sort()
clean_data = numbers + strings
```

### 🟡 Optimized Approach (Pythonic Style)

```python
# Using list comprehensions with type checking
numbers = sorted([x for x in messy_data if isinstance(x, (int, float))])
strings = sorted([x for x in messy_data if isinstance(x, str)])
clean_data = numbers + strings

# Alternative: Using filter() for functional approach
numbers = sorted(filter(lambda x: isinstance(x, (int, float)), messy_data))
strings = sorted(filter(lambda x: isinstance(x, str), messy_data))
clean_data = numbers + strings
```

### 🔴 Advanced Approach (Professional Techniques)

```python
from collections import defaultdict
from operator import methodcaller

# Type-based grouping with defaultdict
def group_by_type(data):
    """Group items by their type."""
    groups = defaultdict(list)
    for item in data:
        groups[type(item)].append(item)
    return dict(groups)

grouped = group_by_type(messy_data)
numbers = sorted(grouped.get(int, []) + grouped.get(float, []))
strings = sorted(grouped.get(str, []))
clean_data = numbers + strings

# Using itertools.groupby with type sorting
from itertools import groupby

# Sort by type first, then group
type_sorted = sorted(messy_data, key=lambda x: (type(x).__name__, x))
type_groups = {k: sorted(list(g)) for k, g in groupby(type_sorted, key=type)}

# Extract and combine
numbers = type_groups.get(int, []) + type_groups.get(float, [])
strings = type_groups.get(str, [])
clean_data = sorted(numbers) + sorted(strings)
```

### 🎯 Key Takeaways

- **Basic**: Manual loops teach type checking fundamentals
- **Optimized**: List comprehensions with `isinstance()` are clean and readable
- **Advanced**: `defaultdict` and `groupby` handle complex grouping scenarios
- **Performance**: List comprehensions are typically faster than manual loops
- **Maintainability**: Type-based grouping scales better for multiple types

### 📊 Performance Notes

- List comprehensions: ~30% faster than manual loops
- `filter()`: Similar performance to comprehensions, more functional style
- `defaultdict`: Excellent for unknown number of groups
- `isinstance()`: Preferred over `type()` for type checking (handles inheritance)
