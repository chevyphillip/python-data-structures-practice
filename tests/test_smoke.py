import glob

import nbformat


def test_notebooks_parse():
    """Ensure every notebook in notebooks/ can be parsed as valid JSON."""
    for path in glob.glob("notebooks/*.ipynb"):
        nbformat.read(path, as_version=4)


def test_basic_structures():
    """Verify core Python data-structure operations function as expected."""
    # List comprehension
    assert [x ** 2 for x in range(1, 6)] == [1, 4, 9, 16, 25]

    # Dictionary comprehension
    assert {i: i ** 2 for i in range(3)} == {0: 0, 1: 1, 2: 4}

    # Set uniqueness
    assert set([1, 2, 2, 3]) == {1, 2, 3}