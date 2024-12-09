To successfully utilize the **Batches** feature in OpenAI, each entry in your JSON Lines (JSONL) file must include specific parameters:

- **`custom_id`**: A unique identifier for each request.
- **`method`**: The HTTP method, typically `"POST"`.
- **`url`**: The API endpoint for the request.
- **`body`**: The request payload, including model details and messages.

Here's how to structure your `batch_prompts.jsonl` file:

```json
{"custom_id": "example_1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4", "messages": [{"role": "system", "content": "Be concise."}, {"role": "user", "content": "Explain AI briefly."}]}}
{"custom_id": "example_2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4", "messages": [{"role": "system", "content": "Be elaborate."}, {"role": "user", "content": "Explain AI in detail."}]}}
```

**Explanation of Parameters:**

- **`custom_id`**: Unique identifier for tracking each request.
- **`method`**: HTTP method; use `"POST"` for sending data.
- **`url`**: API endpoint; for chat completions, it's `"/v1/chat/completions"`.
- **`body`**: Contains the model name and the conversation messages.

**Automating JSONL File Creation:**

If you have multiple prompts, you can automate the creation of the JSONL file using Python:

```python
import json

# List of prompts with unique IDs
prompts = [
    {
        "custom_id": "example_1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Be concise."},
                {"role": "user", "content": "Explain AI briefly."}
            ]
        }
    },
    {
        "custom_id": "example_2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Be elaborate."},
                {"role": "user", "content": "Explain AI in detail."}
            ]
        }
    }
]

# Write the batch to a JSONL file
with open("batch_prompts.jsonl", "w") as file:
    for prompt in prompts:
        file.write(json.dumps(prompt) + "\n")

print("JSONL file created: batch_prompts.jsonl")
```

**Submitting the Batch:**

After preparing your `batch_prompts.jsonl` file, submit it using the OpenAI CLI:

```bash
openai batch create -f batch_prompts.jsonl
```

```bash
openai batch create -m gpt-4 -f prompts.jsonl
```

**Additional Tips:**

- Ensure each `custom_id` is unique to prevent conflicts.
- Validate your JSONL file's structure using tools like `jq`:

  ```bash
  jq . batch_prompts.jsonl
  ```
- Verify your API key and permissions before submission.

By including all required parameters, your batch requests should process without errors.

<br>
