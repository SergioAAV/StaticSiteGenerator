import os

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title
)

def extract_title(markdown) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if not block.startswith("# "):
                raise ValueError("no h1 header found")
            return block[2:].strip()

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file_md = open(from_path, "r")
    markdown = file_md.read()
    file_md.close()
    
    file_template = open(template_path, "r")
    template = file_template.read()
    file_template.close()
    
    node = markdown_to_html_node(markdown)
    html_str = node.to_html()
    
    title = extract_title(markdown)
    temp = template.replace("{{ Title }}", title)
    final = temp.replace("{{ Content }}", html_str)
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    index = open(dest_path, "w")
    index.write(final)
    index.close()