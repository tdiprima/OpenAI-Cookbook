"""
https://github.com/openai/openai-agents-python/tree/main?tab=readme-ov-file#hello-world-example
"""

from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within itself,
# Loops echo through the logic—
# Endless call to start.
