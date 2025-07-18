"""
Takes a directory, grabs its staged diff, asks GPT, and prints back follow‑up suggestions.
Author: tdiprima
"""
import os
import subprocess
import argparse
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_diff_text(path: str) -> str:
    """
    Runs `git diff --cached -- <path>` to get the staged diff for that directory.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--", path],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting diff: {e.stderr}")
        return ""


def suggest_tasks(diff_text: str) -> str:
    prompt = (
        "Here's a git diff:\n\n"
        f"{diff_text}\n\n"
        "What needs follow‑up or could be improved?"
    )
    response = client.chat.completions.create(model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.2)
    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Run TaskSeeker on a staged directory diff")
    parser.add_argument(
        "path",
        help="Path to directory or file to diff (must be staged with `git add`)"
    )
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY in your environment.")
        return

    diff_text = get_diff_text(args.path)
    if not diff_text:
        print("⚠️ No staged changes found for that path.")
        return

    suggestions = suggest_tasks(diff_text)
    print("🕵️‍♂️ TaskSeeker says:\n", suggestions)


if __name__ == "__main__":
    main()
