import os
from pathlib import Path

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    BlockType
)

def extract_title(markdown) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if not block.startswith("# "):
                raise ValueError("no h1 header found")
            return block[2:].strip()

def generate_page(from_path: str, template_path: str, dest_path: str | Path, basepath: str) -> None:
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
    final = final.replace('href="/', f'href="{basepath}')
    final = final.replace('src="/', f'src="{basepath}')
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    index = open(dest_path, "w")
    index.write(final)
    index.close()

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    if not os.path.exists(dir_path_content):
        raise ValueError("content directory doesn't exist")
    for file in os.listdir(dir_path_content):
        path_content = os.path.join(dir_path_content, file)
        path_dest = os.path.join(dest_dir_path, file)
        if os.path.isfile(path_content):
            path_dest = Path(path_dest).with_suffix(".html")
            generate_page(path_content, template_path, path_dest, basepath)
        else:
            generate_pages_recursive(path_content, template_path, path_dest, basepath)
