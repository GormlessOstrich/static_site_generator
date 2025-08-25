import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_pages_recursively(content_dir_path, template_path, dest_dir_path):
    for filename in os.listdir(content_dir_path):
        source_path = os.path.join(content_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(source_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(source_path, template_path, dest_path)
        else:
            generate_pages_recursively(source_path, template_path, dest_path)

def generate_page(source_path, template_path, dest_path):
    print(f" * {source_path} {template_path} -> {dest_path}")
    from_file = open(source_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found.")
