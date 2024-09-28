

class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):

        raise NotImplementedError()
    
    def props_to_html(self):

        props_list = []

        for item in self.props.items():

            props_list.append(f"{item[0]}=\"{item[1]}\"")

        props_string = " ".join(props_list)

        return props_string
    
    def __eq__(self, other_node):

        if self.tag != other_node.tag:
            return False

        if self.value != other_node.value:
            return False

        if self.children != other_node.children:
            return False

        if self.props != other_node.props:
            return False

        return True
    
    

    def __repr__(self):

        formatted_string = f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

        return formatted_string