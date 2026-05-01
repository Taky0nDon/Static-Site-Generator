from __future__ import annotations
class HTMLNode():
    def __init__(self,
                 tag: str=None,
                 value: str=None,
                 children: list[type[HTMLNode]]=None,
                 props: dict[str, str]=None
                 ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        attributes_string = ""
        if self.props is None:
            return attributes_string
        for k,v in self.props.items():
            attributes_string += f' {k}="{v}"'
        return attributes_string

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def __eq__(self, other):
        return (
                self.tag == other.tag,
                self.value == other.value,
                self.children == other.children,
                self.props == other.props,
                )
