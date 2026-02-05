# LangChain LLM test script
from langchain_community.llms import OpenAI

llm = OpenAI(model="gpt-5.2")
print(llm("Hello, gpt-5.2!"))
