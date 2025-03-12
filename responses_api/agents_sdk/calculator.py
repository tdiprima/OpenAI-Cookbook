"""
A Minimal "Calculator" Tool
pip show openai-agents
Author: tdiprima
"""
from agents import Agent, Tool, Runner


def add_numbers(args):
    try:
        a, b = args.split()
        return str(float(a) + float(b))
    except Exception as ex:
        print(ex)
        return "Error: Please pass two numbers separated by a space."


calculator_tool = Tool(
    name="Calculator",
    func=add_numbers,
    description="Adds two numbers (e.g., '3 5')."
)

agent = Agent(
    name="MathTutor",
    instructions=(
        "You are a friendly math tutor. Use the Calculator tool if asked to add."
    ),
    tools=[calculator_tool],
)

result = Runner.run_sync(agent, "What is 2 plus 7?")
print(result.final_output)
