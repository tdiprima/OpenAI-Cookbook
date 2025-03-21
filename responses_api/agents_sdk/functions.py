"""
Functions example
Notice - no LLM in this example
But given this is an official OpenAI SDK, it's very likely using their language models internally
The Agent class is a wrapper around the OpenAI API
https://github.com/openai/openai-agents-python/tree/main?tab=readme-ov-file#functions-example
"""
import asyncio

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    """
    Fake function to get the weather in a city.
    """
    return f"The weather in {city} is sunny."


agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in New York?")
    print(result.final_output)
    # The weather in New York is sunny.


if __name__ == "__main__":
    asyncio.run(main())
