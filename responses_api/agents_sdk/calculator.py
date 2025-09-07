"""
CalcBot with Tool: Parses '[operation] [num1] [num2]' (e.g., 'multiply 6 2'), uses 'do_math' tool for results or 'Error'. Smarter, not harder!
Author: tdiprima
"""

import asyncio

from agents import Agent, Runner, function_tool


# Define the tool for doing math
@function_tool
def do_math(operation: str, num1: float, num2: float) -> str:
    try:
        if operation == "add":
            return str(num1 + num2)
        elif operation == "subtract":
            return str(num1 - num2)
        elif operation == "multiply":
            return str(num1 * num2)
        elif operation == "divide":
            if num2 == 0:
                return "Error"
            return str(num1 / num2)
        else:
            return "Error"
    except Exception:
        return "Error"


# Create the calculator agent with the tool
calc_agent = Agent(
    name="CalcBot",
    instructions="""
    You are a calculator. The user gives you input in the format: '[operation] [number1] [number2]'.
    Supported operations: add, subtract, multiply, divide.
    Use the 'do_math' tool to calculate the result and return only the numerical result (or 'Error' if invalid).
    Examples:
    - 'add 5 3' -> 8
    - 'multiply 4 2' -> 8
    - 'divide 6 0' -> Error
    """,
    tools=[do_math],  # Attach the tool here!
)


# Async function to run the calculator
async def main():
    # Test inputs
    inputs = [
        "add 5 3",  # 8
        "subtract 10 4",  # 6
        "multiply 6 2",  # 12
        "divide 8 2",  # 4
        "divide 5 0",  # Error
        "bad input here",  # Error
    ]

    # Run each input through the agent
    for user_input in inputs:
        result = await Runner.run(calc_agent, input=user_input)
        print(f"Input: {user_input} -> Result: {result.final_output}")


# Run it!
if __name__ == "__main__":
    asyncio.run(main())
