from leafnode import LeafNode
import unittest

class TestLeafNode(unittest.TestCase):

    def test_to_html_full(self):

        test_string = "<a href=\"https://www.google.com\" id=\"link\">Click Me!</a>"
        test_props = {
            "href":  "https://www.google.com",
            "id": "link"
        }

        node = LeafNode("a", "Click Me!", test_props)

        self.assertEqual(node.to_html(), test_string)

    def test_empty_tag(self):

        test_string = "I have no tag!"
        
        node = LeafNode(value="I have no tag!")

        self.assertEqual(node.to_html(), test_string)

    def test_empty_value(self):

        node = LeafNode("p")

        with self.assertRaises(ValueError) as error:
            node.to_html()

            self.assertTrue("Leaf nodes must have a value" in error.exception)

    def test_has_children(self):

        node1 = LeafNode(value="googoo")
        node2 = LeafNode(value="gaagaa")

        test_props = {
            "id": "children"
        }

        with self.assertRaises(TypeError) as error:
            LeafNode("p",  "I shouldn't have children", [node1, node2], test_props)

