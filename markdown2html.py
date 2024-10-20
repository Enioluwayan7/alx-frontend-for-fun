#!/usr/bin/python3
"""
markdown2html.py: A script that converts a Markdown file to an HTML file.
Usage: ./markdown2html.py <input_file.md> <output_file.html>
"""

import sys
import os
import re

def convert_markdown_to_html(input_file, output_file):
    """Convert a Markdown file to HTML and write to an output file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as md_file:
            markdown_lines = md_file.readlines()

        html_lines = []
        inside_unordered_list = False  # Flag to check if we are inside an unordered list
        inside_ordered_list = False    # Flag to check if we are inside an ordered list
        inside_paragraph = False       # Flag to check if we are inside a paragraph

        for line in markdown_lines:
            stripped_line = line.strip()

            # Check for unordered list items
            if stripped_line.startswith("- "):
                if inside_paragraph:
                    html_lines.append("</p>")
                    inside_paragraph = False
                if inside_ordered_list:
                    html_lines.append("</ol>")
                    inside_ordered_list = False
                if not inside_unordered_list:
                    html_lines.append("<ul>")
                    inside_unordered_list = True
                html_lines.append(parse_list_item(stripped_line))

            # Check for ordered list items
            elif stripped_line.startswith("* "):
                if inside_paragraph:
                    html_lines.append("</p>")
                    inside_paragraph = False
                if inside_unordered_list:
                    html_lines.append("</ul>")
                    inside_unordered_list = False
                if not inside_ordered_list:
                    html_lines.append("<ol>")
                    inside_ordered_list = True
                html_lines.append(parse_list_item(stripped_line, ordered=True))

            # Handle paragraph content
            elif stripped_line:
                if inside_unordered_list:
                    html_lines.append("</ul>")
                    inside_unordered_list = False
                if inside_ordered_list:
                    html_lines.append("</ol>")
                    inside_ordered_list = False
                if not inside_paragraph:
                    html_lines.append("<p>")
                    inside_paragraph = True
                html_lines.append(parse_paragraph_line(stripped_line))
            else:
                if inside_paragraph:
                    html_lines.append("</p>")
                    inside_paragraph = False

        # Close any remaining open elements
        if inside_unordered_list:
            html_lines.append("</ul>")
        if inside_ordered_list:
            html_lines.append("</ol>")
        if inside_paragraph:
            html_lines.append("</p>")

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

def parse_list_item(line, ordered=False):
    """
    Convert a single Markdown list item to an HTML <li> element.
    Handles both unordered (- ) and ordered (* ) lists.
    """
    list_item_text = line[2:].strip()  # Remove the "- " or "* " and strip whitespace
    return f"    <li>{list_item_text}</li>"

def parse_paragraph_line(line):
    """
    Convert a single line of a paragraph to HTML.
    Adds <br /> tags for multi-line paragraphs and handles bold/italic formatting.
    """
    line = apply_bold_and_italic(line)  # Convert bold and italic Markdown to HTML
    return f"    {line}<br />" if line.endswith('\n') else f"    {line}"

def apply_bold_and_italic(text):
    """
    Convert Markdown bold (**text**) and italic (__text__) to HTML.
    **text** -> <b>text</b>
    __text__ -> <em>text</em>
    """
    # Replace **text** with <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Replace __text__ with <em>text</em>
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)

    return text

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
