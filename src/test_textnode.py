import unittest
from textnode import TextNode

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

if __name__ == "__main__":
    unittest.main()