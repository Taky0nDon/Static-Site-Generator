import re

import markdown_blocks as md
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnodetohtmlnode import process_text, textnode_to_leafnode

BLOCKTYPE = md.BlockType


def markdown_to_html_node(markdown: str) -> ParentNode:
    md_blocks = md.markdown_to_blocks(markdown)
    child_nodes = []
    for block in md_blocks:
        html_node = block_to_html_node(block)
        child_nodes.append(html_node)
    parent_node = ParentNode(tag="div", children=child_nodes)
    return parent_node


def block_to_html_node(block) -> HTMLNode:
    block_type = md.blocks_to_blocktype(block)
    children = text_to_children(block, block_type)
    match block_type:
        case BLOCKTYPE.PARAGRAPH:
            block = re.sub("\n", " ", block)
            children = []
            tag = "p"
            text_nodes = process_text(block)
            for text_node in text_nodes:
                children.append(text_node_to_html_node(text_node))
        case BLOCKTYPE.HEADING:
            hashes, text = block.split(" ", maxsplit=1)
            size = hashes.count("#")
            tag = f"h{size}"
            text_node = block_to_text_node(block=text, text_type=TextType.TEXT)
            value = text_node_to_html_node(text_node)
        case BLOCKTYPE.CODE:
            return code_block_to_html(block)
        case BLOCKTYPE.QUOTE:
            value = block.lstrip(">").lstrip()
            tag = "blockquote"
        case BLOCKTYPE.UNORDERED_LIST:
            tag = "ul"
            children = text_to_children(block, md.BlockType.UNORDERED_LIST)
        case BLOCKTYPE.ORDERED_LIST:
            tag = "ol"
            children = text_to_children(block, md.BlockType.ORDERED_LIST)
    html_node = ParentNode(tag, children)
    return html_node


def block_to_text_node(block: str, text_type) -> TextNode:
    url = None
    text_node = TextNode(text=block, text_type=text_type, url=url)
    return text_node


def code_block_to_html(block) -> ParentNode:
    code_block = True
    tag = "code"
    value = block
    value = block.strip("`").lstrip()
    html_node = ParentNode("pre", children=[LeafNode(tag="code", value=value)])
    return html_node


def text_to_children(markdown: str, block_type: md.BlockType) -> list[LeafNode]:
    child_html_nodes = []
    match block_type:
        case BLOCKTYPE.PARAGRAPH:
            markdown = markdown.replace("\n", " ")
            for text_node in process_text(markdown):
                child_html_nodes.append(text_node_to_html_node(text_node))
        case BLOCKTYPE.HEADING:
            text_nodes = process_text(markdown.split(" ", maxsplit=1)[-1].strip())
            for node in text_nodes:
                child_html_nodes.append(text_node_to_html_node(node))
        case BLOCKTYPE.QUOTE:
            content = markdown.split(">", maxsplit=1)[-1].strip()
            text_nodes = process_text(content)
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                child_html_nodes.append(html_node)
        case BLOCKTYPE.UNORDERED_LIST | BLOCKTYPE.ORDERED_LIST as list_type:
            if list_type == BLOCKTYPE.ORDERED_LIST:
                lines = markdown.split("\n")
                transitory_md = []
                for line in lines:
                    transitory_md.append(re.sub(r"\d+\.", "- ", line, count=1))
                markdown = "\n".join(transitory_md)

            delimiter = "- "
            lines = markdown.split("\n")
            items = []
            for line in lines:
                item = line.split(delimiter, maxsplit=1)[-1]
                items.append(item)
            for item in items:
                if not item:
                    continue
                text_nodes = process_text(item.strip())
                inner_html_nodes = []
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    inner_html_nodes.append(html_node)
                inner_parent = ParentNode(tag="li", children=inner_html_nodes)
                child_html_nodes.append(inner_parent)

    return [_ for _ in child_html_nodes if _] if child_html_nodes else None
