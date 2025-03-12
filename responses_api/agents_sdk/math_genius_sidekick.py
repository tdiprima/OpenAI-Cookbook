"""
Demonstrates how to add a custom tool and let the agent decide if it needs to use that tool.
pip install openai-agents==0.0.2
Author: tdiprima
"""
from agents import Agent, Tool, Runner


# 1. Define a custom tool. 
#    For a simple example, we'll make a "Calculator" that handles addition.
def add_numbers(arguments):
    """
    Add two numbers. Expects a string with two numbers separated by space.
    Returns their sum as a string.
    """
    try:
        num1_str, num2_str = arguments.split()
        num1, num2 = float(num1_str), float(num2_str)
        return str(num1 + num2)
    except ValueError:
        return "Error: Provide two numbers separated by a space."


calculator_tool = Tool(
    name="Calculator",
    func=add_numbers,
    description="Adds two numbers provided as a string (e.g., '3 5')"
)

# 2. Create an Agent with instructions and give it access to the tool.
my_agent = Agent(
    name="MathTutor",
    instructions=(
        "You are a friendly math tutor. "
        "You can chat about math, and use the Calculator tool to do arithmetic. "
        "If the user asks a question that requires addition, call the Calculator tool."
    ),
    tools=[calculator_tool]
)

# 3. Run a query through the Agent using Runner.
result = Runner.run_sync(my_agent, "What is 4 plus 7?")
print(result.final_output)

# You might see the agent internally decide to call the Calculator tool with "4 7",
# then return: "The answer is 11."
