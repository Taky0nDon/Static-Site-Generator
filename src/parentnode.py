from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self,
                 tag: str,
                 children: list[HTMLNode],
                 props: dict[str, str] = None):
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag.")
        if not self.children:
            raise ValueError("ParentNode must have child nodes.")
        opening = f"<{self.tag}{self.props_to_html()}>"
        closing = f"</{self.tag}>"
        children = "".join(c.to_html() for c in self.children)
        return f"{opening}{children}{closing}"

