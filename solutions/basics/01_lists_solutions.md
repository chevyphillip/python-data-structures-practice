# Solutions: Lists Basics

## Exercise 1: Music Playlist Creation

### Solution

```python
music_data = ["Blinding Lights", "The Weeknd", "Pop", "One Dance", "Drake", "Pop",
              "Bohemian Rhapsody", "Queen", "Rock", "Shape of You", "Ed Sheeran", "Pop"]

# Extract using slicing
songs = music_data[::3]     # [0, 3, 6, 9] -> songs
artists = music_data[1::3]  # [1, 4, 7, 10] -> artists
genres = music_data[2::3]   # [2, 5, 8, 11] -> genres

print("Songs:", songs)
print("Artists:", artists)
print("Genres:", genres)
```

### Key Concepts

- **Slicing syntax**: `[start:stop:step]`
- **Step parameter**: `::3` means "every 3rd item"
- **Starting index**: `[0::3]` vs `[1::3]` vs `[2::3]`

---

## Exercise 2: List Manipulation

### Solution

```python
test_scores = [85, 92, 78, 96, 88, 76, 94, 82, 90, 87]

# Find highest and lowest
highest = max(test_scores)
lowest = min(test_scores)

# Calculate average
average = sum(test_scores) / len(test_scores)

# Filter scores above 90
high_scores = [score for score in test_scores if score > 90]

# Get last 3 scores
last_three = test_scores[-3:]

# Reverse the list
reversed_scores = test_scores[::-1]  # or list(reversed(test_scores))

print(f"Highest: {highest}")
print(f"Lowest: {lowest}")
print(f"Average: {average:.1f}")
print(f"High scores: {high_scores}")
print(f"Last three: {last_three}")
print(f"Reversed: {reversed_scores}")
```

### Alternative Approaches

#### Manual filtering instead of list comprehension

```python
high_scores = []
for score in test_scores:
    if score > 90:
        high_scores.append(score)
```

#### Using built-in functions

```python
high_scores = list(filter(lambda x: x > 90, test_scores))
```

---

## Exercise 3: List Comprehensions

### Solution

```python
# Squares from 1 to 10
squares = [n**2 for n in range(1, 11)]

# Even numbers 0 to 20
evens = [n for n in range(21) if n % 2 == 0]

# Long words (>4 chars)
words = ["cat", "elephant", "dog", "rhinoceros", "bird", "hippopotamus"]
long_words = [word for word in words if len(word) > 4]

# Celsius to Fahrenheit
celsius_temps = [0, 10, 20, 30, 37, 100]
fahrenheit_temps = [(c * 9/5) + 32 for c in celsius_temps]

print(f"Squares: {squares}")
print(f"Evens: {evens}")
print(f"Long words: {long_words}")
print(f"Fahrenheit: {fahrenheit_temps}")
```

### Why List Comprehensions?

- **More readable** than loops for simple operations
- **Faster** than equivalent for loops
- **Pythonic** - idiomatic Python style
