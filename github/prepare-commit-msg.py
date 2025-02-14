"""
Modifies the commit message before Git opens it
python .git/hooks/prepare-commit-msg .git/COMMIT_EDITMSG
Author: tdiprima
"""
import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import sys


def get_git_diff():
    """Fetches the staged git diff."""
    try:
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error fetching git diff: {e}")
        return None


def generate_commit_message(diff):
    """Generates a commit message using OpenAI's GPT API."""
    if not diff:
        return "No changes detected."

    prompt = f"""
    Generate a concise and meaningful commit message based on the following git diff:
    ```
    {diff}
    ```
    """

    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating commit message: {e}")
        return "Auto-generated commit message failed. Please write manually."


def main():
    commit_msg_file = sys.argv[1]  # Path to COMMIT_EDITMSG file
    diff = get_git_diff()
    commit_message = generate_commit_message(diff)

    with open(commit_msg_file, "w") as f:
        f.write(commit_message)


if __name__ == "__main__":
    main()
