from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,
                 tag: str,
                 value: str,
                 props: dict[str, str]=None): 
        """attributes: tag, value, props"""
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        props = self.props_to_html()

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

