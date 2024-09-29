from leafnode import LeafNode

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

        match self.text_type:

            case "text" :
                return LeafNode(value=self.text)
            case "bold":
                return LeafNode("b", self.text)
            case "italic":
                return LeafNode("i", self.text)
            case "code":
                return LeafNode("code", self.text)
            case "link":
                return LeafNode("a", self.text, {"href": self.url})
            case "image":
                return LeafNode("img", "", {"href": self.url, "alt": self.text})
            case _:
                raise ValueError("Invalid text node type")
    
    
    def __repr__(self):

        formated_str = f"TextNode({self.text}, {self.text_type}, {self.url})"

        return formated_str
    
