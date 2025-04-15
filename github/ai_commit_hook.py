"""
Analyze the staged changes and output an AI-generated commit message.
python ai_commit_hook.py /path/to/your/git/repo
Author: tdiprima
"""
import os
import subprocess
import sys

import tiktoken
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def count_tokens(text, model="gpt-4"):
    """Count the number of tokens in the text using tiktoken."""
    try:
        encoder = tiktoken.encoding_for_model(model)
        return len(encoder.encode(text))
    except Exception as e:
        print(f"Error counting tokens: {e}")
        # Return a conservative estimate if token counting fails
        return len(text) // 3


def truncate_diff(diff, max_tokens=8000):
    """Truncate the diff if it exceeds the maximum token limit."""
    prompt_template = """
    Generate a concise and meaningful commit message.
    Subject line (short summary):
    Limit: 50 characters or less.
    Style: Written in the imperative mood (e.g., Add new login endpoint, not Added or Adding).
    No period at the end.
    Generate it based on the following git diff:
    ```
    {}
    ```
    """
    
    # Count tokens in the diff
    prompt_without_diff = prompt_template.format("")
    base_tokens = count_tokens(prompt_without_diff)
    diff_tokens = count_tokens(diff)
    
    # If the diff is already within limits, return it unchanged
    if base_tokens + diff_tokens <= max_tokens:
        return diff, False
    
    # We need to truncate the diff
    # Calculate how many tokens we can use for the diff
    available_tokens = max_tokens - base_tokens
    
    # Split the diff into lines
    diff_lines = diff.split('\n')
    
    # Keep only file headers and mix of beginning and end changes
    truncated_lines = []
    file_headers = []
    
    # Track file headers to maintain context
    for i, line in enumerate(diff_lines):
        if line.startswith('diff --git') or line.startswith('+++') or line.startswith('---'):
            file_headers.append(line)
            diff_lines[i] = None  # Mark as processed
    
    # Remove the processed headers from our counting
    diff_lines = [line for line in diff_lines if line is not None]
    
    # Calculate how many lines to keep from beginning and end
    total_lines = len(diff_lines)
    if total_lines > 0:
        # Keep 70% from beginning, 30% from end if we need to truncate
        beginning_portion = int(available_tokens * 0.7)
        end_portion = available_tokens - beginning_portion
        
        beginning_lines = []
        current_tokens = 0
        
        # Add lines from the beginning until we reach the token limit for this portion
        for line in diff_lines:
            line_tokens = count_tokens(line + '\n')
            if current_tokens + line_tokens <= beginning_portion:
                beginning_lines.append(line)
                current_tokens += line_tokens
            else:
                break
        
        # Add lines from the end until we reach the overall token limit
        end_lines = []
        current_tokens = count_tokens('\n'.join(beginning_lines))
        
        for line in reversed(diff_lines):
            if line in beginning_lines:
                continue
            
            line_tokens = count_tokens(line + '\n')
            if current_tokens + line_tokens <= available_tokens:
                end_lines.insert(0, line)
                current_tokens += line_tokens
            else:
                break
        
        # Combine everything
        all_lines = file_headers + beginning_lines
        
        # Add a separator if we're adding end lines
        if beginning_lines and end_lines:
            all_lines.append("\n[...truncated...]")
        
        all_lines.extend(end_lines)
        
        # Add a note about truncation
        truncation_note = "\n\n[Note: This diff was truncated due to size limitations]"
        truncated_diff = '\n'.join(all_lines) + truncation_note
        
        return truncated_diff, True
    
    return diff, False


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

    # Truncate diff if needed
    truncated_diff, was_truncated = truncate_diff(diff)
    
    if was_truncated:
        print("Warning: The diff was truncated due to token limits.")

    prompt = f"""
    Generate a concise and meaningful commit message based on the following git diff:
    ```
    {truncated_diff}
    ```
    """

    try:
        response = client.chat.completions.create(model="gpt-4o-mini",
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
