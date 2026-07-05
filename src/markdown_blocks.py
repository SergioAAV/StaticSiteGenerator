from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown_block: str) -> BlockType:
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    lines = markdown_block.split("\n")
    if len(lines) > 1 and markdown_block.startswith("```") and markdown_block.endswith("```"):
            return BlockType.CODE
    if markdown_block.startswith(">"):   
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown_block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    final_children = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                paragraph = " ".join(block.split("\n"))
                children = text_to_children(paragraph)
                final_children.append(ParentNode("p", children))
            case BlockType.HEADING:
                count = 0
                for char in block:
                    if char == "#":
                        count += 1
                    else:
                        break
                if count > 6:
                    raise ValueError(f"invalid heading level: {count}")
                text = block[count + 1:]
                children = text_to_children(text)
                final_children.append(ParentNode(f"h{count}", children))
            case BlockType.CODE:
                if not block.startswith("```") or not block.endswith("```"):
                    raise ValueError("invalid code block")
                code_text = block[3:-3].lstrip("\n")
                code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
                final_children.append(ParentNode("pre", [code_node]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                for i in range(len(lines)):
                    if not line[i].startswith(">"):
                        raise ValueError("invalid quote block")
                    lines[i] = lines[i][1:].strip()
                text = " ".join(lines)
                children = text_to_children(text)
                final_children.append(ParentNode("blockquote", children))
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_item = []
                for i in range(len(lines)):
                    lines[i] = lines[i][1:].strip()
                    children = text_to_children(lines[i])
                    list_item.append(ParentNode("li", children))
                final_children.append(ParentNode("ul", list_item))
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_item = []
                for line in lines:
                    line = line.split(". ", 1)
                    text = line[1].strip()
                    children = text_to_children(text)
                    list_item.append(ParentNode("li", children))
                final_children.append(ParentNode("ol", list_item))
            case _:
                raise ValueError("invalid block type")
    return ParentNode("div", final_children)

def text_to_children(text) -> list[HTMLNode]:
    textnodes = text_to_textnodes(text)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    return children