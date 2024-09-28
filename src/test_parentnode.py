from parentnode import ParentNode
from leafnode import LeafNode
import unittest

class TestParentNode(unittest.TestCase):

    def test_to_html_full(self):

        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "Italic text")
        child4 = LeafNode(None, "Normal text")

        child_list1 = [child1, child2]
        child_list2 = [child3, child4]

        parent1 = ParentNode("p", child_list1)
        parent2 = ParentNode("p", child_list2)

        parent_list = [parent1, parent2]

        root = ParentNode("h1", children=parent_list)

        self.assertEqual(root.to_html(), 
                         "<h1><p><b>Bold text</b>Normal text</p><p><i>Italic text</i>Normal text</p></h1>")
        
    def test_no_children(self):

        node = ParentNode("h1", None)

        with self.assertRaises(ValueError) as error:
            node.to_html()
            self.assertTrue("Parent nodes must have children" in error.exception) 

    def test_empty_children(self):

        node = ParentNode("h1", [])

        with self.assertRaises(ValueError) as error:
            node.to_html()
            self.assertTrue("Parent nodes must have children" in error.exception)

    def test_deep_recurse(self):

        test_string = "<html><header><link href=\"/assets/image.png\">image</link></header><body><h1><p><b>Hello, World!</b></p></h1></body></html>"

        link = LeafNode("link", "image", {"href": "/assets/image.png"})
        bold = LeafNode("b", value="Hello, World!")
        
        p = ParentNode("p", [bold])
        h1 = ParentNode("h1", [p])
        body = ParentNode("body", [h1])
        header = ParentNode("header", [link])
        html = ParentNode("html", [header, body])

        self.assertEqual(html.to_html(), test_string)

    def test_many_children(self):

        test_string = "<h1><p>My</p><p>name</p><p>is</p><p>Bryan</p><p>Chappell</p></h1>"
        
        child1 = LeafNode("p", "My")
        child2 = LeafNode("p", "name")
        child3 = LeafNode("p", "is")
        child4 = LeafNode("p", "Bryan")
        child5 = LeafNode("p", "Chappell")

        child_list = [child1, child2, child3, child4, child5]

        root = ParentNode("h1", child_list)

        self.assertEqual(root.to_html(), test_string)