

from textnode import TextNode, TextType
from extract_links import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes,
                          delimiter,
                          text_type: TextType
                          ) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = text.split(delimiter)
            if len(parts) % 2 == 0:
                raise RuntimeError(f"Invalid markdown syntax: {text}")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(
                            TextNode(part, TextType.TEXT)
                            )
                else:
                    new_nodes.append(
                            TextNode(part, text_type)
                            )
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for text_node in old_nodes:
        if text_node.text_type != TextType.TEXT:
            result.append(text_node)
            continue
        alt_text_and_urls = extract_markdown_images(text_node.text)
        if len(alt_text_and_urls) < 1:
            result.append(text_node)
            continue
        reversed_img_tuples = alt_text_and_urls[::-1]
        i = 0
        current_text = []
        while i < len(text_node.text):
            if (text_node.text[i] == "!" and
                i < len(text_node.text) - 1 and
                text_node.text[i + 1] == "["):
                    if current_text:
                        result.append(TextNode("".join(current_text), TextType.TEXT))
                        current_text = []
                    while text_node.text[i] != "]":
                        i += 1
                    if text_node.text[i + 1] != "(":
                         raise RuntimeError(f"No url for image:\n{text_node.text}")
                    while text_node.text[i] != ")":
                        i += 1
                    alt, url = reversed_img_tuples.pop()
                    result.append(TextNode(alt, TextType.IMAGE, url))
            else:
                current_text.append(text_node.text[i])
            i += 1
        if current_text:
            result.append(
                    TextNode("".join(current_text), TextType.TEXT)
                    )
    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for text_node in old_nodes:
        links_and_urls = extract_markdown_links(text_node.text)[::-1]
        parts = text_node.text.split("[")
        for part in parts[1:]:
            if "](" in part:
                link_text, url = links_and_urls.pop()
                result.append(TextNode(link_text, TextType.LINK, url))
                plain_text = part.split(")")[-1]
                if plain_text:
                    result.append(TextNode(plain_text, TextType.TEXT))
            elif part:
                result.append(TextNode(part, TextType.TEXT))
    return result



