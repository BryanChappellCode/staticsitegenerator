import unittest
import functionlibrary as functions
from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from constants import *

display = False

class TestFunctionLibrary(unittest.TestCase):

    def test_split_nodes_delimiter_code(self):

        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = functions.split_nodes_delimiter([node], "`", text_type_code)
        test_list = [TextNode("This is text with a ", text_type_text), TextNode("code block", text_type_code), 
                        TextNode(" word", text_type_text)]
        
        if display:
            print("\nTesting split_nodes_delimiter_code:")
            print(f"Testing with: {node}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(new_nodes, test_list)

    def test_split_nodes_delimiter_bold(self):

        node = TextNode("This is text with a **bold** word", text_type_text)
        new_nodes = functions.split_nodes_delimiter([node], "**", text_type_bold)
        test_list = [TextNode("This is text with a ", text_type_text), TextNode("bold", text_type_bold), 
                        TextNode(" word", text_type_text)]

        if display:
            print("\nTesting split_nodes_delimiter_bold:")
            print(f"Testing with: {node}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(new_nodes, test_list)
    
    def test_split_nodes_delimiter_italic(self):

        node = TextNode("This is text with a *italic* word", text_type_text)
        new_nodes = functions.split_nodes_delimiter([node], "*", text_type_italic)
        test_list = [TextNode("This is text with a ", text_type_text), TextNode(text_type_italic, text_type_italic), 
                        TextNode(" word", text_type_text)]

        if display:
            print("\nTesting split_nodes_delimiter_italic:")
            print(f"Testing with: {node}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(new_nodes, test_list)

    def test_split_nodes_delimiter_unclosed_bold_as_italics(self):

        node = TextNode("Incorrect **amount of delimiters", text_type_text)

        new_nodes = functions.split_nodes_delimiter([node], "*", text_type_italic)
        test_list = [TextNode("Incorrect ", text_type_text), TextNode("", text_type_italic), TextNode("amount of delimiters", text_type_text)]

        if display:
            print("\nTesting split_nodes_delimiter_italic_unclosed_bold_as_italics:")
            print(f"Testing with: {node}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(new_nodes, test_list)

    def test_split_nodes_delimiter_multi_node(self):

        node1 = TextNode("Sentence **One**", text_type_text)
        node2 = TextNode("Sentence **Two**", text_type_text)

        new_nodes = functions.split_nodes_delimiter([node1, node2], "**", text_type_bold)
        test_list = [TextNode("Sentence ", text_type_text), TextNode("One", text_type_bold), TextNode("Sentence ", text_type_text), TextNode("Two", text_type_bold)]
        
        if display:
            print("\nTesting split_nodes_delimiter_multi_node:")
            print(f"Testing with: {[node1, node2]}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(new_nodes, test_list)

    def test_extract_markdown_images(self):

        markdown_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        
        test_list = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        image_list = functions.extract_markdown_images(markdown_string)

        if display:
            print("\nTesting extract_markdown_images:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(image_list, test_list)
   
    def test_extract_markdown_links(self):
    
        markdown_string = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        test_list =  [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        link_list = functions.extract_markdown_links(markdown_string)


        if display:
            print("\nTesting extract_markdown_links:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(link_list, test_list)

    def test_split_nodes_image(self):

        markdown_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        node = TextNode(markdown_string, text_type_text)

        node_list = functions.split_nodes_image([node])

        test_list = [TextNode("This is text with a ", text_type_text), TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", text_type_text), TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")]


        if display:
            print("\nTesting split_nodes_image:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(node_list, test_list)

    def test_split_nodes_link(self):

        markdown_string = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        node = TextNode(markdown_string, text_type_text)

        node_list = functions.split_nodes_link([node])

        test_list = [TextNode("This is text with a link ", text_type_text), 
                     TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                    TextNode(" and ", text_type_text),
                    TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev") ]

        if display:
            print("\nTesting split_nodes_link:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(node_list, test_list)

    def test_split_nodes_link_exclamation(self):

        markdown_string = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"

        node = TextNode(markdown_string, text_type_text)

        node_list = functions.split_nodes_link([node])

        test_list = [TextNode(markdown_string, text_type_text)]


        if display:
            print("\nTesting split_nodes_link_exclamation:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

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

        if display:
            print("\nTesting split_nodes_embedded:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

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

        if display:
            print("\nTesting split_nodes_embedded_reverse:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(embedded_node_list, test_list)


    def test_text_to_textnodes(self):

        markdown_string = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        node_list = functions.text_to_textnodes(markdown_string)
        
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
        if display:
            print("\nTesting text_to_textnodes:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(node_list, test_list)

    def test_text_to_textnodes_error(self):

        markdown_string = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        node_list = functions.text_to_textnodes(markdown_string)
        
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

        if display:
            print("\nTesting text_to_textnodes_error:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

        self.assertNotEqual(node_list, test_list)

    def test_markdown_to_blocks(self):

        markdown_string = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
        markdown_string += "\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        markdown_blocks = functions.markdown_to_blocks(markdown_string)

        test_list = ["# This is a heading", 
                     "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                     "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        
        if display:
            print("\nTesting markdown_to_blocks:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

        self.assertEqual(markdown_blocks, test_list)

    def test_markdown_to_blocks_error(self):

        markdown_string = "# This is a heading\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
        markdown_string += "* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        markdown_blocks = functions.markdown_to_blocks(markdown_string)

        test_list = ["# This is a heading", 
                     "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                     "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        
        if display:
            print("\nTesting markdown_to_blocks_error:")
            print(f"Testing with: {markdown_string}")
            print(f"Verifying with: {test_list}")

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

        if display:
            print("\nTesting block_to_block_type:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

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

        if display:
            print("\nTesting block_to_block_type_heading:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

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

        if display:
            print("\nTesting block_to_block_type_not_heading:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertNotEqual(block_types, test_types)     

    def test_block_to_block_type_code(self):

        block_list = ["``` code block ```",
                      "```\ncode\nblock\n```"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["code", "code"]

        if display:
            print("\nTesting block_to_block_type_code:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_not_code(self):

        block_list = ["``` code block",
                      "````\ncode\nblock\n````"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["code", "code"]

        if display:
            print("\nTesting block_to_block_type_not_code:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertNotEqual(block_types, test_types)

    def test_block_to_block_type_quote(self):

        block_list = [">This is a quote",
                      "> This is a quote",
                      ">This\n>is\n>a\n>quote"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["quote", "quote", "quote"]

        if display:
            print("\nTesting block_to_block_type_quote:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_not_quote(self):

        block_list = ["This is a quote",
                      ">> This is a quote",
                      ">This\nis\na\nquote"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["quote", "quote", "quote"]

        if display:
            print("\nTesting block_to_block_type_not_quote:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertNotEqual(block_types, test_types)

    def test_block_to_block_type_unordered_list(self):

        block_list = ["* This is the first list item in a list block\n* This is a list item\n* This is another list item",
                      "* list!"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["unordered_list", "unordered_list"]

        if display:
            print("\nTesting block_to_block_type_unordered_list:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_not_unordered_list(self):

        block_list = ["* This is the first list item in a list block\n This is a list item\n This is another list item",
                      "** list!"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["unordered_list", "unordered_list"]

        if display:
            print("\nTesting block_to_block_type_not_unordered_list:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertNotEqual(block_types, test_types)

    def test_block_to_block_type_ordered_list(self):

        block_list = ["1. First line\n2. Second line\n3. Third Line"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["ordered_list"]

        if display:
            print("\nTesting block_to_block_type_ordered_list:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertEqual(block_types, test_types)

    def test_block_to_block_type_not_ordered_list(self):

        block_list = ["1. First line\n3. Second line\n4. Third Line"]
        
        block_types = []

        for block in block_list:
            block_types.append(functions.block_to_block_type(block))

        test_types = ["ordered_list"]

        if display:
            print("\nTesting block_to_block_type_not_ordered_list:")
            print(f"Testing with: {block_list}")
            print(f"Verifying with: {test_types}")

        self.assertNotEqual(block_types, test_types)

    def test_markdown_to_html_node(self):

        text = ""
        text = text +  "# This is a heading\n"
        text = text + "\n"
        text = text + "```\n{\n\t\"firstname\": \"John\",\n\t\"lastname\": \"Smith\",\n\t\"age\": 25\n}\n```\n"
        text = text + "\n"
        text = text + "> This is the first line of a quote\n"
        text = text + "> This is the second line of a quote\n"
        text = text + "> This is the third line of a quote\n"
        text = text + "\n"
        text = text + "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
        text = text + "\n"
        text = text + "* This is the first list item in a list block\n"
        text = text + "* This is a list item\n"
        text = text + "* This is another list item\n"
        text = text + "\n"
        text = text + "1. This is the first item in the list\n"
        text = text + "2. This is the second item in the list\n"
        text = text + "3. This is the third item in the list\n"

        markdown = text

        functions.markdown_to_html_node(markdown)

        



