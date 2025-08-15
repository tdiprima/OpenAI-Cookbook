#!/usr/bin/env python3
"""
Script to read a Python file, send it to GPT-5 for explanation, and save the output to output.md
"""

import os
import sys
from pathlib import Path

import typer
from openai import OpenAI
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


def read_python_file(file_path: str) -> str:
    """Read the contents of a Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Python file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")


def explain_code_with_gpt(client: OpenAI, code: str, filename: str) -> str:
    """Send code to GPT-4 for explanation."""
    prompt = f"""Teach me how this Python script works. Please provide a comprehensive explanation that covers:

1. Overall purpose and functionality
2. Key components and their roles  
3. How the code flows and executes
4. Important concepts, algorithms, or patterns used
5. Any notable libraries or techniques employed

Here's the Python code from {filename}:

```python
{code}
```

Please explain it in a clear, educational manner suitable for someone learning Python."""

    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python teacher who explains code clearly and comprehensively.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=4000,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {e}")


def save_explanation(explanation: str, output_file: str = "output.md") -> None:
    """Save the explanation to a markdown file."""
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(f"# Python Code Explanation\n\n")
            file.write(explanation)
        print(f"\n✅ Explanation saved to {output_file}")
    except Exception as e:
        raise Exception(f"Error saving explanation: {e}")


def main(python_file: str = typer.Argument(..., help="Path to the Python file to explain")):
    """Main function to orchestrate the code explanation process."""
    console = Console()

    # Validate input file
    if not Path(python_file).exists():
        console.print(
            f"❌ Error: File '{python_file}' does not exist", style="red"
        )
        raise typer.Exit(1)

    if not python_file.endswith(".py"):
        console.print("⚠️  Warning: File doesn't have .py extension", style="yellow")

    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print(
            "❌ Error: OpenAI API key required. Set OPENAI_API_KEY environment variable",
            style="red",
        )
        raise typer.Exit(1)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:

            # Read the Python file
            task = progress.add_task("Reading Python file...", total=None)
            code = read_python_file(python_file)
            progress.update(task, description="✅ File read successfully")

            # Get explanation from GPT-4
            progress.update(task, description="🤖 Getting explanation from GPT-4...")
            explanation = explain_code_with_gpt(client, code, python_file)
            progress.update(task, description="✅ Explanation received")

            # Save explanation
            progress.update(task, description="💾 Saving explanation...")
            save_explanation(explanation, "output.md")
            progress.update(task, description="✅ Complete!")

        console.print(
            f"\n🎉 Successfully explained '{python_file}'", style="green bold"
        )
        console.print(f"📄 Explanation saved to: output.md")

    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(main)
