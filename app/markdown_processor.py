import markdown2
import os
import re
from datetime import datetime


def get_markdown_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.md')]


def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def parse_markdown_metadata(content):
    lines = content.split('\n')
    metadata = {}
    content_start = 0
    in_metadata = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_metadata:
                in_metadata = True
                continue
            else:
                content_start = i + 1
                break
        if in_metadata and ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip().lower()] = value.strip()

    return metadata, '\n'.join(lines[content_start:])


def markdown_to_html(content):
    return markdown2.markdown(content,
                              extras=[
                                  "fenced-code-blocks",
                                  "tables",
                                  "break-on-newline",
                                  "header-ids",
                                  "smarty-pants",
                              ])


def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse metadata and content
    metadata, markdown_content = parse_markdown_metadata(content)

    # Convert markdown to HTML
    html_content = markdown_to_html(markdown_content)

    title = metadata.get('title',
                         os.path.splitext(os.path.basename(file_path))[0])

    return {
        'title':
        title,
        'slug':
        slugify(title),
        'date':
        metadata.get(
            'date',
            datetime.fromtimestamp(
                os.path.getmtime(file_path)).strftime('%Y-%m-%d')),
        'tags': [
            tag.strip() for tag in metadata.get('tags', '').split(',')
            if tag.strip()
        ],
        'content':
        html_content
    }


def slugify(text):
    # Convert to lowercase
    text = text.lower()
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)
    # Remove all non-word characters (everything except numbers and letters)
    text = re.sub(r'[^\w\-]+', '', text)
    # Replace multiple hyphens with single hyphen
    text = re.sub(r'\-\-+', '-', text)
    # Remove leading and trailing hyphens
    text = text.strip('-')
    return text
