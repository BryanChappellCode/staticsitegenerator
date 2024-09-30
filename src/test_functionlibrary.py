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

    def test_extract_markdown_images(self):

        markdown_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        
        test_list = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        image_list = functions.extract_markdown_images(markdown_string)

        self.assertEqual(image_list, test_list)
   
    def test_extract_markdown_image_more_alt_text(self):

        markdown_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan]"

        with self.assertRaises(Exception) as error:

            image_list = functions.extract_markdown_images(markdown_string)

            self.assertTrue("Invalid syntax for markdown image", error.exception)

    def test_extract_markdown_image_more_links(self):

        markdown_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and (https://i.imgur.com/fJRm4Vk.jpeg)"

        with self.assertRaises(Exception) as error:

            image_list = functions.extract_markdown_images(markdown_string)

            self.assertTrue("Invalid syntax for markdown image", error.exception)

    def test_extract_markdown_image_space_between(self):

        markdown_string = "This is text with a ![rick roll] (https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        with self.assertRaises(Exception) as error:

            image_list = functions.extract_markdown_images(markdown_string)

            self.assertTrue("Invalid syntax for markdown image", error.exception)

    def test_extract_markdown_links(self):
        
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        test_list =  [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        link_list = functions.extract_markdown_links(text)

        self.assertEqual(link_list, test_list)

    def test_extract_markdown_link_more_anchor_text(self):

        markdown_string = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan]"

        with self.assertRaises(Exception) as error:

            image_list = functions.extract_markdown_links(markdown_string)

            self.assertTrue("Invalid syntax for markdown link", error.exception)

    def test_extract_markdown_links_more_links(self):

        markdown_string = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and (https://i.imgur.com/fJRm4Vk.jpeg)"

        with self.assertRaises(Exception) as error:

            image_list = functions.extract_markdown_links(markdown_string)

            self.assertTrue("Invalid syntax for markdown link", error.exception)

    def test_extract_markdown_link_space_between(self):

        markdown_string = "This is text with a [rick roll] (https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        with self.assertRaises(Exception) as error:

            image_list = functions.extract_markdown_links(markdown_string)

            self.assertTrue("Invalid syntax for markdown link", error.exception)

    def test_split_nodes_image(self):

        markdown_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        node = TextNode(markdown_string, text_type_text)

        node_list = functions.split_nodes_image([node])

        test_list = [TextNode("This is text with a ", text_type_text), TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", text_type_text), TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")]

        self.assertEqual(node_list, test_list)

    def test_split_nodes_link(self):

        markdown_string = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        node = TextNode(markdown_string, text_type_text)

        node_list = functions.split_nodes_link([node])

        test_list = [TextNode("This is text with a link ", text_type_text), 
                     TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                    TextNode(" and ", text_type_text),
                    TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev") ]

        self.assertEqual(node_list, test_list)

    def test_split_nodes_link_exclamation(self):

        markdown_string = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"

        node = TextNode(markdown_string, text_type_text)

        node_list = functions.split_nodes_link([node])

        test_list = [TextNode(markdown_string, text_type_text)]

        self.assertEqual(node_list, test_list)

    def test_split_nodes_embedded(self):

        markdown_string = "This is text with a link [to boot dev](https://www.boot.dev) and ![rick roll](https://i.imgur.com/aKaOqIh.gif)"

        node = TextNode(markdown_string, text_type_text)

        node_list = functions.split_nodes_image([node])
        embedded_node_list = functions.split_nodes_link(node_list)

        test_list = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif")
        ]

        self.assertEqual(embedded_node_list, test_list)

    def test_split_nodes_embedded_reverse(self):

        markdown_string = "This is text with a link [to boot dev](https://www.boot.dev) and ![rick roll](https://i.imgur.com/aKaOqIh.gif)"

        node = TextNode(markdown_string, text_type_text)

        node_list = functions.split_nodes_link([node])
        embedded_node_list = functions.split_nodes_image(node_list)

        test_list = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif")
        ]

        self.assertEqual(embedded_node_list, test_list)