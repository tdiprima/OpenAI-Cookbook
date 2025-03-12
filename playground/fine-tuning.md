## [Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)

To meet the requirement of at least **10 examples** for fine-tuning, you can expand your dataset with diverse input-output pairs. Here's how to ensure you have enough examples:


### Step 1: Create 10 Examples
Below is an expanded dataset with at least 10 entries for fine-tuning a **translation assistant**:

```json
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: Hello"}, {"role": "assistant", "content": "Bonjour"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: Goodbye"}, {"role": "assistant", "content": "Au revoir"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: Thank you"}, {"role": "assistant", "content": "Merci"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: Please"}, {"role": "assistant", "content": "S'il vous plaît"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: Excuse me"}, {"role": "assistant", "content": "Excusez-moi"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: I love you"}, {"role": "assistant", "content": "Je t'aime"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: How are you?"}, {"role": "assistant", "content": "Comment ça va?"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: Good morning"}, {"role": "assistant", "content": "Bonjour"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: Good night"}, {"role": "assistant", "content": "Bonne nuit"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant that translates text to French."}, {"role": "user", "content": "Translate to French: See you later"}, {"role": "assistant", "content": "À plus tard"}]}
```


### Step 2: Automate Dataset Creation
If you want to generate more examples programmatically:

#### Python Code:

```python
import json

# Create a list of examples
examples = [
    {"input": "Hello", "output": "Bonjour"},
    {"input": "Goodbye", "output": "Au revoir"},
    {"input": "Thank you", "output": "Merci"},
    {"input": "Please", "output": "S'il vous plaît"},
    {"input": "Excuse me", "output": "Excusez-moi"},
    {"input": "I love you", "output": "Je t'aime"},
    {"input": "How are you?", "output": "Comment ça va?"},
    {"input": "Good morning", "output": "Bonjour"},
    {"input": "Good night", "output": "Bonne nuit"},
    {"input": "See you later", "output": "À plus tard"}
]

# Convert to chat format
chat_data = []
for idx, example in enumerate(examples):
    chat_data.append({
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that translates text to French."},
            {"role": "user", "content": f"Translate to French: {example['input']}"},
            {"role": "assistant", "content": example['output']}
        ]
    })

file_name = "training_data.jsonl"

# Save to JSONL file
with open(file_name, "w") as file:
    for entry in chat_data:
        file.write(json.dumps(entry) + "\n")

print("Dataset with 10 examples created:", file_name)
```


### Step 3: Validate and Upload the Dataset
1. **Validate the JSONL file**:

   ```bash
   jq . training_data.jsonl
   ```

2. **Upload the file**:

   ```bash
   openai file upload --purpose fine-tune -f training_data.jsonl
   ```

3. **Start Fine-Tuning**:

   [How to fine tune a model using terminal](https://community.openai.com/t/how-to-fine-tune-a-model-using-terminal/)

   ```bash
   openai api fine_tunes.create -t file-<file-id> -m gpt-3.5-turbo-0125
   ```


### Step 4: Testing the Fine-Tuned Model
Once fine-tuning is complete, test the model by querying it:

```python
response = client.chat.completions.create(model="your-fine-tuned-model-id",
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Translate to French: I am happy"}
])
print(response.choices[0].message.content)
```

<br>
