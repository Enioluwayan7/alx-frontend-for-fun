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
            markdown_lines = md_file.readlines()

        html_lines = []
        inside_list = False  # Flag to check if we are inside a list

        for line in markdown_lines:
            # Check for list items
            if line.startswith("- "):
                if not inside_list:
                    html_lines.append("<ul>")  # Start the unordered list
                    inside_list = True
                html_lines.append(parse_list_item(line))
            else:
                if inside_list:
                    html_lines.append("</ul>")  # Close the unordered list
                    inside_list = False
                html_lines.append(parse_markdown_line(line))  # Parse other Markdown syntax

        # If the document ends while still inside a list, close the list
        if inside_list:
            html_lines.append("</ul>")

        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write('\n'.join(html_lines))

    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

def parse_markdown_line(line):
    """
    Convert a single line of Markdown to HTML.
    Supports heading levels from 1 to 6.
    """
    heading_level = line.count('#', 0, 6)  # Count leading '#' symbols (max 6)
    
    if heading_level > 0 and line.startswith('#' * heading_level + ' '):
        heading_text = line[heading_level:].strip()
        return f"<h{heading_level}>{heading_text}</h{heading_level}>"
    else:
        return line.strip()  # For now, return non-heading lines as plain text

def parse_list_item(line):
    """
    Convert a single Markdown list item to an HTML <li> element.
    """
    list_item_text = line[2:].strip()  # Remove the "- " and strip whitespace
    return f"    <li>{list_item_text}</li>"

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
