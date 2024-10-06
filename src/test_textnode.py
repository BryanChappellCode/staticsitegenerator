import unittest
import functionlibrary as functions
from textnode import TextNode
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a Text Node", "bold")
        self.assertNotEqual(node1, node2)

    def test_url_eq(self):
        node1 = TextNode("Testing the URL", "italics", "https://github.com/BryanChappellCode/staticsitegenerator")
        node2 = TextNode("Testing the URL", "italics", "https://github.com/BryanChappellCode/staticsitegenerator")
        self.assertEqual(node1, node2)

    def test_url_not_eq(self):
        node1 = TextNode("Testing the URL", "italics", "https://github.com/BryanChappellCode/staticsitegenerator")
        node2 = TextNode("Testing the URL", "italics")
        self.assertNotEqual(node1, node2)

    def test_type_not_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italics")
        self.assertNotEqual(node1, node2)

    def test_text_to_html(self):

        text_node = TextNode("Test", "text")
        leaf_node = functions.text_node_to_html_node(text_node)

        test_node = LeafNode(value="Test")

        self.assertEqual(leaf_node, test_node)

    def test_bold_to_html(self):

        text_node = TextNode("Test", "bold")
        leaf_node = functions.text_node_to_html_node(text_node)

        test_node = LeafNode("b", "Test")

        self.assertEqual(leaf_node, test_node)

    def test_italic_to_html(self):

        text_node = TextNode("Test", "italic")
        leaf_node = functions.text_node_to_html_node(text_node)

        test_node = LeafNode("i", "Test")

        self.assertEqual(leaf_node, test_node)

    def test_code_to_html(self):

        text_node = TextNode("Test", "code")
        leaf_node = functions.text_node_to_html_node(text_node)

        test_node = LeafNode("code", "Test")

        self.assertEqual(leaf_node, test_node)

    def test_link_to_html(self):

        text_node = TextNode("Test", "link", "www.google.com")
        leaf_node = functions.text_node_to_html_node(text_node)

        test_node = LeafNode("a", "Test", {"href": "www.google.com"})

        self.assertEqual(leaf_node, test_node)

    def test_image_to_html(self):

        text_node = TextNode("Test", "image", "/assets/image.png")
        leaf_node = functions.text_node_to_html_node(text_node)

        test_node = LeafNode("img", "", {"href": "/assets/image.png", "alt": "Test"})

        self.assertEqual(leaf_node, test_node)

    def test_invalid_type(self):

        text_node = TextNode("h1", "Header")
        
        with self.assertRaises(ValueError) as error:
            
            functions.text_node_to_html_node(text_node)
            self.assertTrue("Invalid text node type", error.exception)
            

if __name__ == "__main__":
    unittest.main()