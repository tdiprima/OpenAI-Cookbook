"""
Using openai-agents to summarize latest papers on Alzheimer's treatment
Author: tdiprima
"""

from agents import Agent, Runner

query = "Summarize latest papers on Alzheimer's treatment"

# instructions = """
# You are a research assistant specializing in summarizing medical papers.
# Given a research topic, your goal is to:
# 1. Find 3-5 recent research papers from reliable sources like PubMed or Arxiv.
# 2. Summarize each paper's key findings in 3-4 sentences.
# 3. Highlight any significant breakthroughs or controversies.
# 4. If applicable, provide practical implications in simple terms.
# """

instructions = """
You are an AI-powered research assistant. Your task is to:
- Search for the latest research papers on the given topic.
- Retrieve relevant abstracts.
- Summarize the key points, including:
  - The study's objective
  - Main findings
  - Potential impact
- If multiple papers are found, compare and contrast them.

Topic: {query}
"""

# Create the research assistant agent with the specified model
research_assistant = Agent(
    name="Research Assistant",
    instructions=instructions,
    # model="gpt-5.2"  # Specify the model here
)

result = Runner.run_sync(research_assistant, query)
print(result.final_output)
