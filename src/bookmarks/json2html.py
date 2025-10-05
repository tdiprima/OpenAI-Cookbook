"""
Use this script to convert a JSON file to HTML (to import into Chrome bookmarks)
Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = "tdiprima"
__version__ = "1.0"
__license__ = "MIT"

import json


def json_to_html(json_file, html_file):
    with open(json_file, "r", encoding="utf-8") as file:
        categories = json.load(file)

    with open(html_file, "w", encoding="utf-8") as file:
        # Write the standard HTML header for bookmarks
        file.write("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n")
        file.write(
            '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
        )
        file.write("<TITLE>Bookmarks</TITLE>\n")
        file.write("<H1>Bookmarks</H1>\n")
        file.write("<DL><p>\n")

        # Write categories and bookmarks
        for category, bookmarks in categories.items():
            file.write(f"    <DT><H3>{category}</H3>\n")
            file.write("    <DL><p>\n")
            for bookmark in bookmarks:
                file.write(
                    f'        <DT><A HREF="{bookmark["url"]}">{bookmark["name"]}</A>\n'
                )
            file.write("    </DL><p>\n")

        file.write("</DL><p>\n")


# Replace these filenames with your actual paths
json_file = "organized_bookmarks.json"
html_file = "organized_bookmarks.html"

json_to_html(json_file, html_file)
print(f"Bookmarks exported to '{html_file}'.")
