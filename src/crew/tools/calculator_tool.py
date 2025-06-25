import json
import ast
import operator
from crewai.tools import tool

class CalculatorTools:
    @tool("Make a calculation")
    def calculate(input_string: str) -> str:
        """
        Evaluate a math expression passed as a JSON string.
        Example input: '{"expression": "8000 + (6 * 2500) + (7 * 1200) + (7 * 400) + (7 * 750)"}'
        
        Args:
            input_string (str): JSON string containing the math expression
            
        Returns:
            str: The calculation result or error message
        """
        try:
            # Step 1: Parse JSON string
            data = json.loads(input_string)
            expression = data.get("expression")

            if not expression:
                return "❌ Error: No 'expression' key found in input."

            # Step 2: Safely evaluate the expression using AST (safer than eval)
            result = safe_eval(expression)
            return f"Result: {result}"

        except json.JSONDecodeError as e:
            return f"❌ Error: Input is not valid JSON. {str(e)}"
        except Exception as e:
            return f"❌ Calculation Error: {str(e)}"


def safe_eval(expression: str):
    """
    Safely evaluate mathematical expressions using AST
    Only allows basic math operations: +, -, *, /, //, %, **
    """
    # Supported operations
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def eval_node(node):
        if isinstance(node, ast.Constant):  # Numbers
            return node.value
        elif isinstance(node, ast.Num):  # For older Python versions
            return node.n
        elif isinstance(node, ast.BinOp):  # Binary operations
            left = eval_node(node.left)
            right = eval_node(node.right)
            op = operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op)}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):  # Unary operations like -5
            operand = eval_node(node.operand)
            op = operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operation: {type(node.op)}")
            return op(operand)
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode='eval')
        # Evaluate the AST
        return eval_node(tree.body)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


# Test the tool
if __name__ == "__main__":
    calc_tool = CalculatorTools()
    
    # Test with your example input
    test_input = '{"expression": "8000 + (6 * 2500) + (7 * 1200) + (7 * 400) + (7 * 750)"}'
    result = calc_tool.calculate(test_input)
    print(f"Input: {test_input}")
    print(f"Output: {result}")
    
    # Additional tests
    test_cases = [
        '{"expression": "10 + 5 * 2"}',
        '{"expression": "100 / 4"}',
        '{"expression": "2 ** 3"}',
        '{"expression": "15 % 4"}',
        '{"invalid": "10 + 5"}',  # Should fail - no expression key
        '{"expression": "10 + abc"}',  # Should fail - invalid expression
    ]
    
    for test in test_cases:
        print(f"\nTest: {test}")
        print(f"Result: {calc_tool.calculate(test)}")