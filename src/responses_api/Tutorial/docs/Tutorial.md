Below is a tutorial for the three main tools announced in OpenAI's Agents Tools Launch: the **Responses API**, **Web Search**, and **File Search**.

---

## Tutorial: Getting Started with OpenAI's New Agent Tools

### 1. Responses API – Building Smarter Conversations
**What it does**: The Responses API combines the strengths of Chat Completions and Assistants APIs, enabling AI agents to execute tasks automatically and integrate results into conversations. It's designed as a scalable foundation for interactive agents.

**Tutorial**:

- **Step 1: Setup**  
  Ensure you have an OpenAI API key. Install the OpenAI SDK (e.g., `pip install openai` for Python).
  
- **Step 2: Basic Request**  
  Use the Responses API to send a user query and let it handle tool execution. Here's a simple example:

  ```python
  import openai

  client = openai.OpenAI(api_key="your-api-key")
  response = client.responses.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": "What's the weather like today?"}],
      tools=["web_search"]  # Automatically triggers web search if needed
  )
  print(response.choices[0].message.content)
  ```

  The API detects when a tool (like web search) is required, executes it, and appends the result to the conversation.

- **Step 3: Customize Tools**  
  Add built-in tools (e.g., web search, file search) or define custom ones. The API manages execution and context seamlessly.

- **Key Tip**: Use this for agents that need to adapt and learn from task results over time. Check the OpenAI docs for the full tool list and schema.

---

### 2. Web Search Tool – Fetching Real-Time Answers
**What it does**: This tool integrates web search into your AI agent, providing cited, up-to-date results. It works with `gpt-4o` and `gpt-4o-mini` in the Responses API or Chat Completions API (preview mode).

**Tutorial**:

- **Step 1: Enable Web Search**  
  In the Responses API, specify the `web_search` tool (as shown above). For Chat Completions API:

  ```python
  response = client.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": "Latest AI news"}],
      tools=[{"type": "web_search"}]
  )
  print(response.choices[0].message.content)
  ```

- **Step 2: Handle Follow-Ups**  
  The tool supports conversational follow-ups. Try this:

  ```python
  response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
          {"role": "user", "content": "Latest AI news"},
          {"role": "assistant", "content": response.choices[0].message.content},
          {"role": "user", "content": "Tell me more about the top story"}
      ],
      tools=[{"type": "web_search"}]
  )
  ```

  It'll refine the search and respond contextually.

- **Step 3: Check Citations**  
  Results include sources (e.g., URLs). Access them via the response metadata if available (check preview docs for exact format).

- **Key Tip**: Use this for agents needing real-time info (e.g., news, weather). It's in preview, so expect updates—test thoroughly!

---

### 3. File Search Tool – Digging Through Documents
**What it does**: This tool searches documents (PDFs, text files, etc.) quickly, with advanced features like reranking and query rewriting. It's available in both Responses API and Assistants API.

**Tutorial**:

- **Step 1: Upload Files**  
  First, upload files to OpenAI's storage (Assistants API context):

  ```python
  file = client.files.create(
      file=open("document.pdf", "rb"),
      purpose="assistants"
  )
  ```

- **Step 2: Search Files**  
  In Responses API:

  ```python
  response = client.responses.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": "Summarize my PDF"}],
      tools=[{"type": "file_search", "file_ids": [file.id]}]
  )
  print(response.choices[0].message.content)
  ```

  Or in Assistants API:

  ```python
  assistant = client.beta.assistants.create(
      model="gpt-4o",
      tools=[{"type": "file_search"}],
      file_ids=[file.id]
  )
  thread = client.beta.threads.create(
      messages=[{"role": "user", "content": "Summarize my PDF"}]
  )
  run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
  # Poll for completion, then retrieve result
  ```

- **Step 3: Advanced Features**  
  Experiment with filtering (e.g., by date) or reranking for better results—details are in the API docs.

- **Key Tip**: Ideal for agents processing internal docs or knowledge bases. Preprocess files for best performance (e.g., clean text, split large PDFs).

---

## Final Notes
- **Agents SDK**: The announcement mentions this open-source toolkit for building and monitoring agents, but no specific usage details are provided. Check the OpenAI GitHub or docs for setup instructions—it's bonus tooling for scaling your projects.
- **Next Steps**: Combine these tools! For example, use Web Search for live data and File Search for static docs in one agent via the Responses API.
- **Need More?**: If you want deeper code examples, specific use cases, or integration with the Agents SDK, let me know what you're building!

---

# Nope.

`file_snipe.py` doesn't work.

Based on my research of the available documentation, I've discovered that:

- The Responses API is indeed new and is meant to combine features of Chat Completions and Assistants APIs
- There seems to be some confusion about vector stores in the documentation
- The `file_search` tool is available, but the implementation details in the documentation are incomplete

Given this, I think we have two options:

1. Use the Assistants API instead, which has well-documented file handling capabilities
2. Try a simpler approach with the Responses API using just file search


After all these attempts, I can conclude that:

- The Responses API requires vector stores for file search
- The vector store functionality seems to be in development or not fully documented yet
- For now, we should probably use the Assistants API instead, which has well-documented file handling capabilities

Answer: `file_snipe_assist.py`


## Quote of the day

We're tougher than a bug in prod on a Friday night. 💪

<br>
