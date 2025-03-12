"""
Need help: cannot import name 'Agent' from 'agents' (openai-agents==0.0.3)
https://platform.openai.com/docs/guides/agents
https://openai.github.io/openai-agents-python/
"""
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
