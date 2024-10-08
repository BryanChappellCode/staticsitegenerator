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


    def test_text_to_textnodes(self):

        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        node_list = functions.text_to_textnodes(text)
        
        test_list = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ]

        self.assertEqual(node_list, test_list)

    def test_text_to_textnodes_error(self):

        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        node_list = functions.text_to_textnodes(text)
        
        test_list = [
            TextNode("This is", text_type_text),
            TextNode("text", text_type_bold),
            TextNode("with an", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode("word and a", text_type_text),
            TextNode("code block", text_type_code),
            TextNode("and an", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("and a", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ]

        self.assertNotEqual(node_list, test_list)

    def test_markdown_to_blocks(self):

        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
        markdown += "\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        markdown_blocks = functions.markdown_to_blocks(markdown)

        test_list = ["# This is a heading", 
                     "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                     "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        
        self.assertEqual(markdown_blocks, test_list)

    def test_markdown_to_blocks_error(self):

        markdown = "# This is a heading\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
        markdown += "* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        markdown_blocks = functions.markdown_to_blocks(markdown)

        test_list = ["# This is a heading", 
                     "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                     "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        
        self.assertNotEqual(markdown_blocks, test_list)

    def test_block_to_block_type(self):

        block_list = ["# This is a heading", 
                     "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                     "``` This is a code block ```",
                     ">This is a quote\n> This is also a quote",
                     "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
                     "1. First line\n2. Second line\n3. Third Line"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["heading", "paragraph", "code", "quote", "unordered_list", "ordered_list"]

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_heading(self):

        block_list = ["# This is a heading", 
                     "## This is a heading",
                     "### This is a heading",
                     "#### This is a heading",
                     "##### This is a heading",
                     "###### This is a heading"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["heading", "heading", "heading", "heading", "heading", "heading"]

        self.assertEqual(block_types, test_types)   
        
    def test_block_to_block_type_not_heading(self):

        block_list = ["#This is a heading", 
                     "##This is a heading",
                     "###This is a heading",
                     "####This is a heading",
                     "#####This is a heading",
                     "######This is a heading",
                     "####### This is a heading",
                     "This is a heading"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["heading", "heading", "heading", "heading", "heading", "heading", "heading", "heading"]

        self.assertNotEqual(block_types, test_types)     

    def test_block_to_block_type_code(self):

        block_list = ["``` code block ```",
                      "```\ncode\nblock\n```"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["code", "code"]

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_not_code(self):

        block_list = ["``` code block",
                      "````\ncode\nblock\n````"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["code", "code"]

        self.assertNotEqual(block_types, test_types)

    def test_block_to_block_type_quote(self):

        block_list = [">This is a quote",
                      "> This is a quote",
                      ">This\n>is\n>a\n>quote"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["quote", "quote", "quote"]

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_not_quote(self):

        block_list = ["This is a quote",
                      ">> This is a quote",
                      ">This\nis\na\nquote"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["quote", "quote", "quote"]

        self.assertNotEqual(block_types, test_types)

    def test_block_to_block_type_unordered_list(self):

        block_list = ["* This is the first list item in a list block\n* This is a list item\n* This is another list item",
                      "* list!"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["unordered_list", "unordered_list"]

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_not_unordered_list(self):

        block_list = ["* This is the first list item in a list block\n This is a list item\n This is another list item",
                      "** list!"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["unordered_list", "unordered_list"]

        self.assertNotEqual(block_types, test_types)

    def test_block_to_block_type_ordered_list(self):

        block_list = ["1. First line\n2. Second line\n3. Third Line"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["ordered_list"]

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_not_ordered_list(self):

        block_list = ["1. First line\n3. Second line\n4. Third Line"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["ordered_list"]

        self.assertNotEqual(block_types, test_types)