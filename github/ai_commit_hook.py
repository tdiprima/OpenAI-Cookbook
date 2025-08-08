"""
Analyze the staged changes and output an AI-generated commit message.
python ai_commit_hook.py /path/to/your/git/repo
Author: tdiprima
"""
import os
import subprocess
import sys

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o"


def get_git_diff(repo_path):
    """Fetches the staged git diff for the given repository."""
    try:
        result = subprocess.run(["git", "-C", repo_path, "diff", "--cached"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error fetching git diff: {e}")
        return None


def generate_commit_message(diff):
    """Generates a commit message using OpenAI's GPT API."""
    if not diff:
        return "No changes detected."

    prompt = f"""
    Here's a git diff. Generate a concise and professional Git commit message based on the changes. Use the Conventional Commits style.
    RESPONSES MUST BE <= 50 CHARACTERS LONG.

    Diff:
    ```
    {diff}
    ```
    """

    try:
        response = client.chat.completions.create(model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating commit message: {e}")
        return "Auto-generated commit message failed. Please write manually."


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_git_repo>")
        sys.exit(1)

    repo_path = sys.argv[1]
    diff = get_git_diff(repo_path)
    commit_message = generate_commit_message(diff)

    print(commit_message)


if __name__ == "__main__":
    main()
