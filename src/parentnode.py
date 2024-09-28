from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):

        if self.tag == None:
            raise ValueError("Parent nodes must have a tag")
        
        if self.children == None or len(self.children) == 0:
            raise ValueError("Parent nodes must have children")
        
        child_string = ""
        
        for child in self.children:
            child_string += child.to_html()

        if self.props == None:
            return f"<{self.tag}>{child_string}</{self.tag}>"

        return f"<{self.tag} {self.props_to_html()}>{child_string}</{self.tag}>"