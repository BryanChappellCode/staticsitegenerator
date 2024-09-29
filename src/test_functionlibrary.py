import unittest
import functionlibrary as functions
from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from constants import *

class TestFunctionLibrary(unittest.TestCase):

    def test_split_nodes_delimiter_code(self):

        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = functions.split_nodes_delimiter([node], "`", text_type_code)
        test_list = [TextNode("This is text with a ", text_type_text), TextNode("code block", text_type_code), 
                        TextNode(" word", text_type_text)]

        self.assertEqual(new_nodes, test_list)

    def test_split_nodes_delimiter_bold(self):

        node = TextNode("This is text with a **bold** word", text_type_text)
        new_nodes = functions.split_nodes_delimiter([node], "**", text_type_bold)
        test_list = [TextNode("This is text with a ", text_type_text), TextNode("bold", text_type_bold), 
                        TextNode(" word", text_type_text)]

        self.assertEqual(new_nodes, test_list)
    
    def test_split_nodes_delimiter_italic(self):

        node = TextNode("This is text with a *italic* word", text_type_text)
        new_nodes = functions.split_nodes_delimiter([node], "*", text_type_italic)
        test_list = [TextNode("This is text with a ", text_type_text), TextNode(text_type_italic, text_type_italic), 
                        TextNode(" word", text_type_text)]

        self.assertEqual(new_nodes, test_list)

    def test_split_nodes_delimiter_invalid(self):
        
        node = TextNode("Invalid", text_type_text)

        with self.assertRaises(ValueError) as error:
            new_nodes = functions.split_nodes_delimiter([node], "^", text_type_bold)

            self.assertTrue("Invalid delimiter", error.exception)

    def test_split_nodes_delimiter_italic_mismatch(self):
        
        node = TextNode("Invalid", text_type_text)

        with self.assertRaises(ValueError) as error:
            new_nodes = functions.split_nodes_delimiter([node], "*", text_type_bold)

            self.assertTrue("Asterisk delimiter must correspond to italic type", error.exception)
    
    def test_split_nodes_delimiter_bold_mismatch(self):
        
        node = TextNode("Invalid", text_type_text)

        with self.assertRaises(ValueError) as error:
            new_nodes = functions.split_nodes_delimiter([node], "**", text_type_italic)

            self.assertTrue("Double asterisk delimiter must correspond to bold type", error.exception)

    def test_split_nodes_delimiter_code_mismatch(self):
        
        node = TextNode("Invalid", text_type_text)

        with self.assertRaises(ValueError) as error:
            new_nodes = functions.split_nodes_delimiter([node], "`", text_type_italic)

            self.assertTrue("Backtick delimiter must correspond to code type", error.exception)

    def test_split_nodes_delimiter_unclosed(self):

        node = TextNode("Incorrect **amount of delimiters", text_type_text)

        with self.assertRaises(Exception) as error:
            new_nodes = functions.split_nodes_delimiter([node], "**", text_type_bold)

            self.assertTrue("Unclosed delimiter", error.exception)

    def test_split_nodes_delimiter_unclosed_bold_as_italics(self):

        node = TextNode("Incorrect **amount of delimiters", text_type_text)

        new_nodes = functions.split_nodes_delimiter([node], "*", text_type_italic)
        test_list = [TextNode("Incorrect ", text_type_text), TextNode("", text_type_italic), TextNode("amount of delimiters", text_type_text)]

        self.assertEqual(new_nodes, test_list)

    def test_split_nodes_delimiter_multi_node(self):

        node1 = TextNode("Sentence **One**", text_type_text)
        node2 = TextNode("Sentence **Two**", text_type_text)

        new_nodes = functions.split_nodes_delimiter([node1, node2], "**", text_type_bold)
        test_list = [TextNode("Sentence ", text_type_text), TextNode("One", text_type_bold), TextNode("Sentence ", text_type_text), TextNode("Two", text_type_bold)]
        
        self.assertEqual(new_nodes, test_list)