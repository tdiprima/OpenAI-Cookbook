"""
JokeBot: Tells a short joke. Simple LLM-only agent.
Author: tdiprima
"""
from agents import Agent, Runner

joke_bot = Agent(name="JokeBot", instructions="Tell me a short joke.")
result = Runner.run_sync(joke_bot, "Gimme a laugh!")
print(result.final_output)
# Why don't skeletons fight each other?
# They don't have the guts!
