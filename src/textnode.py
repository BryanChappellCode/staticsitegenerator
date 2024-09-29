from leafnode import LeafNode
from constants import *

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):

        if self.text != other_node.text:
            return False

        if self.text_type != other_node.text_type:
            return False
        
        if self.url != other_node.url:
            return False

        return True
    
    def text_node_to_html_node(self):

        if self.text_type == text_type_text: return LeafNode(value=self.text)
        if self.text_type == text_type_bold: return LeafNode("b", self.text)
        if self.text_type == text_type_italic: return LeafNode("i", self.text)
        if self.text_type == text_type_code: return LeafNode("code", self.text)
        if self.text_type == text_type_link: return LeafNode("a", self.text, {"href": self.url})
        if self.text_type == text_type_image: return LeafNode("img", "", {"href": self.url, "alt": self.text})

        raise ValueError("Invalid text node type")

    def __repr__(self):

        formated_str = f"TextNode({self.text}, {self.text_type}, {self.url})"

        return formated_str
    
