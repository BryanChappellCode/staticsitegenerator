import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):

        prop_dict = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }

        node = HTMLNode(props=prop_dict)
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\"")

    def test_eq(self):

        prop_dict = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }

        node1 = HTMLNode("h1", "val", HTMLNode(), prop_dict)
        node2 = HTMLNode("h1", "val", HTMLNode(), prop_dict)

        self.assertEqual(node1, node2)

    def test_tag_not_eq(self):

        node1 = HTMLNode(tag="h2")
        node2 = HTMLNode(tag="h1")

        self.assertNotEqual(node1, node2)

    def test_val_not_eq(self):

        node1 = HTMLNode(value="Hello World!")
        node2 = HTMLNode(value="hello world!")

        self.assertNotEqual(node1, node2)

    def test_child_not_eq(self):

        child1 = HTMLNode()
        child2 = HTMLNode()

        node1 = HTMLNode(children=child1)
        node2 = HTMLNode(children=child2)

        self.assertNotEqual(node1, node2)

    def test_val_not_eq(self):

        props1= {
            "href": "https://www.google.com", 
            "target": "_blank",
        }

        props2= {
            "href": "https://www.yahoo.com", 
            "target": "_blank",
        }

        node1 = HTMLNode(props=props1)
        node2 = HTMLNode(props=props2)

        self.assertNotEqual(node1, node2)
    
    