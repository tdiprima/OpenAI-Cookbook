"""
A Minimal "Calculator" Tool Using LangChain
Author: tdiprima
"""
from langchain.agents import Tool, AgentType
from langchain.agents import initialize_agent
from langchain_openai import OpenAI


def add_numbers(input_str: str) -> str:
    try:
        a, b = input_str.split()
        return str(float(a) + float(b))
    except Exception as ex:
        print(ex)
        return "Error: Please pass two numbers separated by a space."


tools = [
    Tool(
        name="Calculator",
        func=add_numbers,
        description="Adds two numbers. E.g., '3 5' -> '8'"
    ),
]

# An LLM to power the agent
llm = OpenAI(temperature=0)

# Note: Consider migrating to LangGraph for new projects as it offers more flexibility
# and features including tool-calling, state persistence, and human-in-the-loop workflows.
# See: https://langchain-ai.github.io/langgraph/

# Build the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use it
print(agent.invoke({"input": "What is 2 plus 7?"})["output"])
