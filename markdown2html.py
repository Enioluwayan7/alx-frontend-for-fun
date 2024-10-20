#!/usr/bin/python3
"""
markdown2html.py: A script that converts a Markdown file to an HTML file.
Usage: ./markdown2html.py <input_file.md> <output_file.html>
"""

import sys
import os

def convert_markdown_to_html(input_file, output_file):
    """Convert a Markdown file to HTML and write to an output file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()

        # Basic conversion from Markdown to HTML (can be extended with more features)
        html_content = markdown_content.replace("# ", "<h1>").replace("\n", "<br>")

        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    if not os.path.exists(input_filename):
        print(f"Missing {input_filename}", file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(input_filename, output_filename)
    sys.exit(0)
