from agents import Agent, Runner

query = "Summarize latest papers on Alzheimer's treatment"

instructions = """
You are a research assistant specializing in summarizing medical papers. 
Given a research topic, your goal is to:
1. Find 3-5 recent research papers from reliable sources like PubMed or Arxiv.
2. Summarize each paper's key findings in 3-4 sentences.
3. Highlight any significant breakthroughs or controversies.
4. If applicable, provide practical implications in simple terms.
"""

research_assistant = Agent(name="Research Assistant", instructions=instructions)
result = Runner.run_sync(research_assistant, query)
print(result.final_output)
