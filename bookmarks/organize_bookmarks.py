"""
Export your bookmarks from Chrome and use this script to categorize them
Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = "tdiprima"
__version__ = "1.0"
__license__ = "MIT"

import json
import os

from bs4 import BeautifulSoup
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_bookmarks(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    bookmarks = []
    for tag in soup.find_all("a"):
        bookmarks.append({"name": tag.text, "url": tag["href"]})
    return bookmarks


def categorize_bookmarks(bookmarks):
    categories = {}
    for bookmark in bookmarks:
        response = client.chat.completions.create(
            model="gpt-4o-realtime-preview-2025-06-03",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that categorizes URLs into short labels.",
                },
                {
                    "role": "user",
                    "content": f"Categorize this URL: {bookmark['url']}. Provide a short label (e.g., Tech, News, Shopping).",
                },
            ],
            max_tokens=10,
        )
        category = response.choices[0].message.content.strip()
        if category not in categories:
            categories[category] = []
        categories[category].append(bookmark)
    return categories


def save_categories(categories, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(categories, file, indent=4)


# Replace with your exported bookmarks file
bookmarks_file = "bookmarks.html"
bookmarks = parse_bookmarks(bookmarks_file)
categorized = categorize_bookmarks(bookmarks)
save_categories(categorized, "organized_bookmarks.json")

print("Bookmarks organized and saved to 'organized_bookmarks.json'")
