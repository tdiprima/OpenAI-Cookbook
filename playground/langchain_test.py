# LangChain LLM test script
from langchain_community.llms import OpenAI

llm = OpenAI(model="gpt-4o-mini")
print(llm("Hello, gpt-4o!"))
