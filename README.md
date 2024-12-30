# Conditional Operator Inverter

This script inverts the conditional operators in a given Python code snippet. It uses the `ast` module to parse the code and a custom `NodeTransformer` class to invert the operators.

## Prerequisites

Before running the code, please make sure to install the required `astor` package by running the following command:

```sh
pip install astor
```

## Usage

The script takes a Python code snippet as input and inverts the conditional operators in the code. It includes automated tests to verify the correctness of the inversion.

### Example

Here is an example usage of the script:

```python
example_code = """x = 10
y = 5

while x <= 0 and x < 0:
    x = x + 5
    print("x increased by 5")

if x >= y and x != 0:
    print("x is greater than y and x is not zero")
else:
    print("x is less than y or x is zero")
"""

# Process the code
operator_positions, inverted_code = invert_conditionals_and_output(example_code)

# Print the results
print("\nOperator positions:", operator_positions)
print("\nInverted code:\n")
print(inverted_code)
```

### Output

The script will output the positions of the inverted operators and the transformed code with the inverted operators.

## Automated Tests

The script includes automated tests to verify the correctness of the inversion. The tests can be run by calling the run_tests function.

### Example Tests

```python
def test_inversion():
    test_code = """if x < y:
    pass
if x != y:
    pass"""
    expected_operators = [((1, 3), 'Lt'), ((3, 3), 'NotEq')]
    expected_code = """if x >= y:
    pass
if x == y:
    pass"""

    positions, inverted = invert_conditionals_and_output(test_code)
    assert positions == expected_operators, f"Expected {expected_operators}, got {positions}"
    assert inverted.strip() == expected_code.strip(), f"Expected:\n{expected_code}\nGot:\n{inverted}"
    print("All tests passed!")

def test_nested_conditions():
    test_code = """if x < y and y != z:
    pass"""
    expected_operators = [((1, 3), 'Lt'), ((1, 13), 'NotEq')]  # Updated column position
    expected_code = """if x >= y and y == z:
    pass"""

    positions, inverted = invert_conditionals_and_output(test_code)
    assert positions == expected_operators, f"Expected {expected_operators}, got {positions}"
    assert inverted.strip() == expected_code.strip(), f"Expected:\n{expected_code}\nGot:\n{inverted}"
    print("Nested conditions test passed!")

def test_no_conditions():
    test_code = """x = 5
y = 10
print(x + y)"""
    expected_operators = []
    expected_code = """x = 5
y = 10
print(x + y)"""

    positions, inverted = invert_conditionals_and_output(test_code)
    assert positions == expected_operators, f"Expected no operators, got {positions}"
    assert inverted.strip() == expected_code.strip(), f"Expected:\n{expected_code}\nGot:\n{inverted}"
    print("No conditions test passed!")

# Run tests
def run_tests():
    test_inversion()
    test_nested_conditions()
    test_no_conditions()

run_tests()
```
