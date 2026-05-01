from textnode import TextNode, TextType

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




