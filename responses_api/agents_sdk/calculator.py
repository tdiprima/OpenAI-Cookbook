"""
Calculator Agent: Takes '[operation] [num1] [num2]' (e.g., 'add 5 3'), returns result or 'Error'. Pure LLM vibes, no tools!
Author: tdiprima
"""
import asyncio
from agents import Agent, Runner

# Create the calculator agent
calc_agent = Agent(
    name="CalcBot",
    instructions="""
    You are a calculator. The user will give you an input in the format: '[operation] [number1] [number2]'.
    Supported operations: add, subtract, multiply, divide.
    Return only the numerical result. If the input is invalid or division by zero occurs, return 'Error'.
    Examples:
    - 'add 5 3' -> 8
    - 'multiply 4 2' -> 8
    - 'divide 6 0' -> Error
    """,
)


# Async function to run the calculator
async def main():
    # Test inputs (you can change these!)
    inputs = [
        "add 5 3",            # Should return 8
        "subtract 10 4",      # Should return 6
        "multiply 6 2",       # Should return 12
        "divide 8 2",         # Should return 4
        "divide 5 0",         # Should return Error
        "bad input here",     # Should return Error
    ]

    # Run each input through the agent
    for user_input in inputs:
        result = await Runner.run(calc_agent, input=user_input)
        print(f"Input: {user_input} -> Result: {result.final_output}")

# Run it!
if __name__ == "__main__":
    asyncio.run(main())
