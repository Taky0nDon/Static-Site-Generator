from textnode import TextNode, TextType
from leafnode import LeafNode
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link

def process_text(original_text: str) -> list[TextNode]:
    starting_node = TextNode(original_text, TextType.TEXT)
    starting_nodes = [starting_node]
    for text_type, delimiter in zip(
            [TextType.CODE, TextType.BOLD, TextType.ITALIC,],
            [ "`", "**", "_",]
            ):
        starting_nodes = split_nodes_delimiter(starting_nodes, delimiter, text_type)
    starting_nodes = split_nodes_image(starting_nodes)
    starting_nodes = split_nodes_link(starting_nodes)
    return starting_nodes

def textnode_to_leafnode(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(
                    value=text_node.text)
        case TextType.BOLD:
            return LeafNode(
                    value=text_node.text,
                    tag="b")
        case TextType.ITALIC:
            return LeafNode(
                    value=text_node.text,
                    tag="i"
                    )
        case TextType.LINK:
            return LeafNode(
                    value=text_node.text,
                    tag="a",
                    props={
                        "href": text_node.url
                        }
                    )
        case TextType.IMAGE:
            return LeafNode(
                    value=text_node.text,
                    tag="img",
                    props={"src": text_node.url,
                           "alt": text_node.text,
                           },
                    )
        case TextType.CODE:
            return LeafNode(
                    value=text_node.text,
                    tag="code"
                    )


