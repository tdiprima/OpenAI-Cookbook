"""
Demonstrates how the agent can interpret a request ("double the number 5") and delegate to a tool
Author: tdiprima
"""
from agents import Agent, Runner, Tool


# Define a simple tool that doubles a number
def double_number(number: int) -> int:
    """Doubles the input number."""
    return number * 2


# Create a tool instance
double_tool = Tool(
    name="double",
    description="Doubles a given number",
    func=double_number
)

# Create an agent with the tool
agent = Agent(
    name="MathHelper",
    instructions="You are a helpful math assistant. Use the 'double' tool when asked to double a number, or provide general help otherwise."
)

# Run the agent with a request
result = Runner.run_sync(
    agent,
    "Can you double the number 5 for me?"
)

# Print the result
print(result.final_output)
