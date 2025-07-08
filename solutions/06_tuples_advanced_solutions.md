# Solutions: Tuples Advanced

## Exercise 1: Employee Data Management

### Solution

```python
employee_records = [
    ('Alice Johnson', 'Software Engineer', 95000, 'Engineering'),
    ('Bob Chen', 'Data Scientist', 98000, 'Analytics'),
    ('Carol Davis', 'Product Manager', 105000, 'Product'),
    ('David Wilson', 'Software Engineer', 92000, 'Engineering'),
    ('Emma Brown', 'UX Designer', 78000, 'Design')
]

# Extract all employee names
employee_names = [name for name, _, _, _ in employee_records]

# Find high earners (>$95,000)
high_earners = [record for record in employee_records if record[2] > 95000]

# Calculate average salary by department
dept_salaries = {}
for name, position, salary, department in employee_records:
    if department not in dept_salaries:
        dept_salaries[department] = []
    dept_salaries[department].append(salary)

avg_by_dept = {dept: sum(salaries)/len(salaries) 
               for dept, salaries in dept_salaries.items()}

# Engineer name-salary pairs
engineer_salaries = [(name, salary) for name, position, salary, dept 
                     in employee_records if position == 'Software Engineer']

print(f"Employee names: {employee_names}")
print(f"High earners: {high_earners}")
print(f"Average salary by department: {avg_by_dept}")
print(f"Engineer salaries: {engineer_salaries}")
```

### Key Concepts

- **Tuple Unpacking**: Using `name, position, salary, department = record` to extract values
- **Underscore Convention**: Using `_` for unused variables in unpacking
- **List Comprehensions with Tuples**: Filtering and transforming tuple data efficiently

### Common Mistakes

1. **Forgetting Tuple Immutability**: Trying to modify tuple elements
   ```python
   # Incorrect approach
   employee_records[0][2] = 100000  # TypeError!
   
   # Correct approach
   new_record = (employee_records[0][0], employee_records[0][1], 100000, employee_records[0][3])
   ```

2. **Index Confusion**: Hard-coding indices instead of unpacking
   ```python
   # Less readable
   names = [record[0] for record in employee_records]
   
   # More readable
   names = [name for name, _, _, _ in employee_records]
   ```

---

## Exercise 2: Coordinate Geometry

### Solution

```python
import math

coordinates = [(0, 0), (3, 4), (6, 8), (1, 1), (-2, 3), (5, -2)]

def distance_from_origin(point):
    x, y = point
    return math.sqrt(x**2 + y**2)

# Calculate distances
distances = [distance_from_origin(point) for point in coordinates]

# Find farthest point
farthest_point = max(coordinates, key=distance_from_origin)

# Sort by distance
sorted_by_distance = sorted(coordinates, key=distance_from_origin)

# Identify quadrants
def get_quadrant(point):
    x, y = point
    if x > 0 and y > 0: return "Q1"
    elif x < 0 and y > 0: return "Q2"
    elif x < 0 and y < 0: return "Q3"
    elif x > 0 and y < 0: return "Q4"
    else: return "Origin/Axis"

quadrants = {}
for point in coordinates:
    quadrant = get_quadrant(point)
    if quadrant not in quadrants:
        quadrants[quadrant] = []
    quadrants[quadrant].append(point)
```

### Alternative Approaches

#### Using defaultdict for cleaner grouping

```python
from collections import defaultdict

quadrants = defaultdict(list)
for point in coordinates:
    quadrant = get_quadrant(point)
    quadrants[quadrant].append(point)
```

#### Functional approach with groupby

```python
from itertools import groupby

# Sort first, then group
sorted_coords = sorted(coordinates, key=get_quadrant)
quadrants = {k: list(g) for k, g in groupby(sorted_coords, key=get_quadrant)}
```

### Performance Considerations

- **Time Complexity**: O(n log n) for sorting, O(n) for other operations
- **Space Complexity**: O(n) for storing results
- **Best Practice**: Use `key` parameter with built-in functions like `max()` and `sorted()`

---

## Exercise 3: Named Tuples

### Solution

```python
from collections import namedtuple

# Create Student named tuple
Student = namedtuple('Student', ['name', 'grades', 'major', 'year'])

# Create student records
students = [
    Student('Alice Johnson', [3.8, 3.9, 3.7, 3.6], 'Computer Science', 2024),
    Student('Bob Chen', [3.6, 3.7, 3.5, 3.8], 'Data Science', 2025),
    Student('Carol Davis', [3.9, 4.0, 3.8, 3.9], 'Computer Science', 2024),
    Student('David Wilson', [3.4, 3.6, 3.5, 3.7], 'Mathematics', 2026),
    Student('Emma Brown', [3.7, 3.8, 3.6, 3.9], 'Data Science', 2025)
]

# Calculate GPA for each student
def calculate_gpa(grades):
    return sum(grades) / len(grades) if grades else 0.0

student_gpas = [(student.name, calculate_gpa(student.grades)) 
                for student in students]

# Group by major and calculate average GPA
major_gpas = {}
for student in students:
    if student.major not in major_gpas:
        major_gpas[student.major] = []
    major_gpas[student.major].append(calculate_gpa(student.grades))

avg_gpa_by_major = {major: sum(gpas)/len(gpas) 
                    for major, gpas in major_gpas.items()}
```

### Why Named Tuples?

Named tuples provide:
- **Readability**: `student.name` vs `student[0]`
- **Immutability**: Same benefits as regular tuples
- **Memory Efficiency**: Less memory than dictionaries
- **Attribute Access**: Dot notation for field access

---

## Challenge Exercise: Data Pipeline Processing

### Solution

```python
from collections import namedtuple

sensor_data = [
    (1609459200, 'temp_01', 23.5, 'ok'),
    (1609459260, 'temp_01', 24.1, 'ok'),
    (1609459320, 'temp_02', 22.8, 'error'),
    (1609459380, 'temp_01', 25.2, 'ok'),
    (1609459440, 'temp_02', 23.9, 'ok')
]

# Filter valid readings
valid_readings = [reading for reading in sensor_data if reading[3] == 'ok']

# Group by sensor
sensor_groups = {}
for timestamp, sensor_id, value, status in valid_readings:
    if sensor_id not in sensor_groups:
        sensor_groups[sensor_id] = []
    sensor_groups[sensor_id].append(value)

# Calculate statistics and create summary tuples
SensorSummary = namedtuple('SensorSummary', ['sensor_id', 'count', 'min_val', 'max_val', 'avg_val'])

summaries = []
for sensor_id, values in sensor_groups.items():
    summary = SensorSummary(
        sensor_id=sensor_id,
        count=len(values),
        min_val=min(values),
        max_val=max(values),
        avg_val=sum(values) / len(values)
    )
    summaries.append(summary)
```

### Solution Breakdown

1. **Filtering**: Remove error readings using list comprehension
2. **Grouping**: Build dictionary mapping sensor IDs to value lists
3. **Statistics**: Calculate min, max, average for each sensor
4. **Summary Creation**: Use named tuples for structured output

### Why This Approach?

- **Immutable Data**: Tuples prevent accidental data modification
- **Functional Style**: Each step transforms data without side effects
- **Type Safety**: Named tuples provide structure and documentation
- **Memory Efficient**: Tuples use less memory than objects

### Extensions

For further practice, try:
- Adding timestamp-based filtering (e.g., last hour only)
- Calculating rolling averages using sliding windows
- Implementing outlier detection using statistical methods
- Creating a data validation pipeline with custom status codes

---

## Learning Summary

### What You've Learned

- Tuple unpacking for clean, readable code
- Using tuples for immutable data records
- Named tuples for structured data with attribute access
- Functional programming patterns with tuples
- Grouping and aggregation techniques

### Real-World Applications

- **Database Records**: Representing table rows as tuples
- **Coordinate Systems**: 2D/3D points in graphics and mapping
- **Data Pipelines**: Immutable data transformation stages
- **Configuration Data**: Settings that shouldn't change
- **API Responses**: Structured data from external services

### Next Steps

- Explore tuple methods like `count()` and `index()`
- Practice with nested tuples for complex data structures
- Learn about tuple performance optimizations
- Connect to: Advanced data structures (trees, graphs using tuples)