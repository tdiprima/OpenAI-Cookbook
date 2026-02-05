import time

import openai

# Set up the client
client = openai.OpenAI()

# Upload your file
with open("ai_trends_2025.pdf", "rb") as file:
    uploaded_file = client.files.create(file=file, purpose="assistants")
print(f"File uploaded: {uploaded_file.id} 🎉")

# Create a basic assistant with file search
assistant = client.beta.assistants.create(
    name="File Sniper",
    instructions="You're a pro at digging answers out of files!",
    model="gpt-5.2",
    tools=[{"type": "file_search"}],
)
print(f"Assistant ready: {assistant.id} 🦸‍♂️")

# Start a thread and ask your question
thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's the top AI prediction for 2025 in this doc?",
    attachments=[{"file_id": uploaded_file.id, "tools": [{"type": "file_search"}]}],
)
print(f"Question asked in thread: {thread.id} 💬")

# Run the assistant
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
print(f"Run started: {run.id} ⚡")

# Wait for it... with a timeout and status updates!
start_time = time.time()
timeout = 30  # 30 seconds max
while run.status not in ("completed", "failed"):
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"Status: {run.status} ⏳")
    if time.time() - start_time > timeout:
        print("Timeout! Run's taking too long—check the file or API! 😵")
        break
    time.sleep(1)

# Check the result
if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print("Answer:", messages.data[0].content[0].text.value)  # Victory! 🎉
elif run.status == "failed":
    print(f"Run failed! Reason: {run.last_error} ❌")  # Spill the error!
else:
    print(f"Run stopped with status: {run.status} 🤔")
