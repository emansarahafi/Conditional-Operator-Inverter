"""
Done by: Eman Sarah Afi

Before running the code, please make sure to install the required astor package by running the following command:
pip install astor

This script:
- Takes a Python code snippet as input and inverts the conditional operators in the code.
- Uses the ast module to parse the code and then inverts the operators using a custom NodeTransformer class.
- Includes automated tests to verify the correctness of the inversion.

"""

import ast
import astor

# Map for operator inversion
INVERT_OPERATORS = {
    ast.Lt: ast.GtE,  # < becomes >=
    ast.LtE: ast.Gt,  # <= becomes >
    ast.Gt: ast.LtE,  # > becomes <=
    ast.GtE: ast.Lt,  # >= becomes <
    ast.Eq: ast.NotEq,  # == becomes !=
    ast.NotEq: ast.Eq,  # != becomes ==
}

class ConditionalInverter(ast.NodeTransformer):
    def __init__(self):
        self.operator_positions = []

    def visit_Compare(self, node):
        # Visit and modify Compare nodes
        for idx, op in enumerate(node.ops):
            if type(op) in INVERT_OPERATORS:
                start_pos = (node.lineno, node.col_offset + idx)
                self.operator_positions.append((start_pos, op.__class__.__name__))
                node.ops[idx] = INVERT_OPERATORS[type(op)]()
        self.generic_visit(node)
        return node

# Function to process code
def invert_conditionals_and_output(code):
    # Parse the code
    tree = ast.parse(code)
    inverter = ConditionalInverter()
    
    # Transform the AST
    transformed_tree = inverter.visit(tree)
    ast.fix_missing_locations(transformed_tree)

    # Get the transformed code
    inverted_code = astor.to_source(transformed_tree)

    return inverter.operator_positions, inverted_code

# Example usage
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

# Automated tests
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