"""
https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat&lang=python
"""

from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-5.2",
    # web_search_options={},
    messages=[
        {
            "role": "user",
            "content": "Find a recent PubMed article on Major Depression. Summarize it in a way that a 10th grader can understand. List citations.",
        }
    ],
)

print(completion.choices[0].message.content)
