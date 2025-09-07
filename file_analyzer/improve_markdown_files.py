"""
Improve the README file

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = "tdiprima"
__version__ = "1.0"
__license__ = "MIT"

import os

from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Directory containing Markdown files
home_directory = os.environ["HOME"]
MARKDOWN_DIR = home_directory + "/path/to/your/markdown"
OUTPUT_DIR = home_directory


def improve_markdown(file_path, output_path):
    """
    Read a Markdown file, send its content to GPT-4 for improvement, and save the response.
    """
    with open(file_path, "r") as file:
        content = file.read()

    print(f"Processing: {file_path}")

    # Construct the OpenAI prompt
    prompt = f"""You are a skilled editor. I will provide you with some Markdown content.
    Your task is to rewrite and improve it while keeping the original meaning intact.
    Make the writing clearer, smoother, and more engaging.
    Preserve the structure and formatting of Markdown.
    Correct any grammar, spelling, or style issues.
    Do not change the intent or factual content.

    Here is the Markdown content:
    {content}
    """

    try:
        # Call GPT-4
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in writing and improving markdown content.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Extract improved content
        improved_content = response.choices[0].message.content

        # Save the improved content to the output file
        with open(output_path, "w") as output_file:
            output_file.write(improved_content)

        print(f"Improved content saved to: {output_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def process_markdown_files(input_dir, output_dir):
    """
    Process all Markdown files in the input directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all markdown files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".md"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            improve_markdown(input_path, output_path)


if __name__ == "__main__":
    process_markdown_files(MARKDOWN_DIR, OUTPUT_DIR)
