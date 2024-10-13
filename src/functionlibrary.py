from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from constants import *
import re

def text_node_to_html_node(text_node):

        if text_node.text_type == text_type_text: return LeafNode(value=text_node.text)
        if text_node.text_type == text_type_bold: return LeafNode("b", text_node.text)
        if text_node.text_type == text_type_italic: return LeafNode("i", text_node.text)
        if text_node.text_type == text_type_code: return LeafNode("code", text_node.text)
        if text_node.text_type == text_type_link: return LeafNode("a", text_node.text, {"href": text_node.url})
        if text_node.text_type == text_type_image: return LeafNode("img", "", {"href": text_node.url, "alt": text_node.text})

        raise ValueError("Invalid text node type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):


    new_node_list = []

    if delimiter not in ["*", "**", "`"]: 
        raise ValueError("Invalid delimiter")
    elif delimiter == "*" and text_type != text_type_italic:
        raise ValueError("Asterisk delimiter must correspond to italic type")
    elif delimiter == "**" and text_type != text_type_bold:
        raise ValueError("Double asterisk delimiter must correspond to bold type")
    elif delimiter == "`" and text_type != text_type_code:
        raise ValueError("Backtick delimiter must correspond to code type")
    

    for node in old_nodes:

        node_list = []

        if node.text_type != text_type_text:
    
            new_node_list.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0: raise Exception("Unclosed delimiter")

        oscillator = text_type_text

        for text in split_text:
            node_list.append(TextNode(text, oscillator))
            if oscillator == text_type_text: oscillator = text_type
            else: oscillator = text_type_text

        # trim empty tags from ends
        if node_list[0].text == "": 
            del node_list[0]   
                
        if node_list[-1].text == "":
            del node_list[-1]

        new_node_list.extend(node_list)


    return new_node_list

def extract_markdown_images(text):

    alt_text = re.findall("(?:[!]{1}\[(.*?)\]\(.*?\))" , text)
    links = re.findall("(?:[!]{1}\[.*?\]\((.*?)\))" , text)

    if len(alt_text) != len(links):
        raise Exception("Invalid syntax for markdown image")

    image_list = []

    for i in range(0, len(alt_text)):

        valid_syntax = f"![{alt_text[i]}]({links[i]})"
    
        if valid_syntax not in text:
            raise Exception("Invalid syntax for markdown image")
        
        image_list.append((alt_text[i], links[i]))

    return image_list

def extract_markdown_links(text):
    
    anchor_text = re.findall("(?:[^!]\[(.*?)\]\(.*?\))" , text)
    links = re.findall("(?:[^!]\[.*?\]\((.*?)\))" , text)

    pass
    if len(anchor_text) != len(links):
        raise Exception("Invalid syntax for markdown link: Unpaired anchor text/link")

    link_list = []

    for i in range(0, len(anchor_text)):

        valid_syntax = f"[{anchor_text[i]}]({links[i]})"
    
        if valid_syntax not in text:
            raise Exception("Invalid syntax for markdown link: Anchor text must be joined with link")
        
        link_list.append((anchor_text[i], links[i]))

    return link_list

def split_nodes_image(old_nodes):

    new_node_list = []

    for node in old_nodes:

        if node.text_type != text_type_text:
            new_node_list.append(node)
            continue

        node_list = []
        image_list = extract_markdown_images(node.text)
        delimited_text = re.sub("([!]\[.*?\]\(.*?\))", "*", node.text)
        split_text = delimited_text.split("*")
        
        # Since the image markdown is used as a delimiter, there will always be one less object in the image list than the text list
        if len(split_text) - 1 != len(image_list):
            raise Exception("Invalid markdown syntax")

        # Since every other node will be text, oscillate between a text node and an image node
        oscillator = text_type_text
        j = 0
        k = 0

        # Loop for the sum of objects of both lists. Add text, then image. Text, then image. And so on...
        for i in range(0, len(split_text) + len(image_list)):

            if oscillator == text_type_text:
                node_list.append(TextNode(split_text[j], text_type_text))
                oscillator = text_type_image
                j += 1
            else:
                alt_text = image_list[k][0]
                url = image_list[k][1]
                node_list.append(TextNode(alt_text, text_type_image, url))
                oscillator = text_type_text
                k += 1
        
        # trim empty nodes
        if node_list[0].text == "": del node_list[0]
        if node_list[-1].text == "": del node_list[-1]

        new_node_list.extend(node_list)
    
    return new_node_list
        
def split_nodes_link(old_nodes):

    new_node_list = []

    for node in old_nodes:

        if node.text_type != text_type_text:
            new_node_list.append(node)
            continue

        node_list = []
        link_list = extract_markdown_links(node.text)
        delimited_text = re.sub("(?<=[^!])(\[.*?\]\(.*?\))", "*", node.text)
        split_text = delimited_text.split("*")

        # Since the link markdown is used as a delimiter, there will always be one less object in the link list than the text list
        if len(split_text) - 1 != len(link_list):
            raise Exception("Invalid markdown syntax")

        # Since every other node will be text, oscillate between a text node and an image node
        oscillator = text_type_text
        j = 0
        k = 0

        # Loop for the sum of objects of both lists. Add text, then image. Text, then image. And so on...
        for i in range(0, len(split_text) + len(link_list)):

            if oscillator == text_type_text:
                node_list.append(TextNode(split_text[j], text_type_text))
                oscillator = text_type_link
                j += 1
            else:
                anchor_text = link_list[k][0]
                url = link_list[k][1]
                node_list.append(TextNode(anchor_text, text_type_link, url))
                oscillator = text_type_text
                k += 1
        
        # trim empty nodes
        if node_list[0].text == "": del node_list[0]
        if node_list[-1].text == "": del node_list[-1]

        new_node_list.extend(node_list)
    
    return new_node_list

def text_to_textnodes(text):

    text_list = [TextNode(text, text_type_text)]

    bold_list = split_nodes_delimiter(text_list, "**", text_type_bold)
    italic_list = split_nodes_delimiter(bold_list, "*", text_type_italic)
    code_list = split_nodes_delimiter(italic_list, "`", text_type_code)
    image_list = split_nodes_image(code_list)
    link_list = split_nodes_link(image_list)

    return link_list

def markdown_to_blocks(markdown):

    split_markdown = markdown.split("\n\n")

    block_list = []

    for block in split_markdown:
        block_list.append(block.strip())

    return block_list

def block_to_block_type(block):

    pattern = re.search("^[#]{1,6}[\s][a-zA-Z0-9\s]*", block)

    if pattern != None:
        return "heading"

    pattern = re.search("^[`]{3}[\s\S]*[`]{3}$", block)

    if pattern != None:
        return "code"

    pattern = re.search("^[>]", block)

    if pattern != None:

        split_pattern = block.split("\n")

        for line in split_pattern:
            line_pattern = re.search("^[>]", block)

            if line_pattern == None:
                return "paragraph"

        return "quote"

    pattern = re.search("^[*][\s]", block)

    if pattern != None:

        split_pattern = block.split("\n")

        for line in split_pattern:
            line_pattern = re.search("^[*][\s]", block)

            if line_pattern == None:
                return "paragraph"

        return "unordered_list"

    i = 1

    pattern = re.search(f"^[{i}][.][\s]", block)

    if pattern != None:

        split_pattern = block.split("\n")

        for line in split_pattern:

            line_pattern = re.search(f"^[{i}][.][\s]", line)

            if line_pattern == None:
                return "paragraph"
            
            i += 1
        
        return "ordered_list"
    
    return "paragraph"

def markdown_to_html_node(markdown):

    markdown_blocks = markdown_to_blocks(markdown)

    html_list = []

    for block in markdown_blocks:
        markdown_type = block_to_block_type(block)    
        html_list.append(create_markdown_html_node(block, markdown_type))
    
    full_html = ParentNode("div", html_list)

    return full_html

def create_markdown_html_node(markdown_text, markdown_type):

    match markdown_type:
        case "heading":
            return create_heading_node(markdown_text)
        case "code":
            return create_code_node(markdown_text)
        case "quote":
            return create_quote_node(markdown_text)
        case "ordered_list":
            return create_ordered_list_node(markdown_text)
        case "unordered_list":
            return create_unordered_list_node(markdown_text)
        case "paragraph":
            return create_paragraph_node(markdown_text)
        case _:
            raise Exception(f"Invalid markdown type: {markdown_type}")

def create_heading_node(heading):
    
    split_heading_block = heading.split("\n")

    if len(split_heading_block) > 1:
        raise Exception("Only one line per heading block allowed")

    split_line = heading.split()
    head_num = len(split_line[0])
    heading_text = " ".join(split_line[1:])

    heading_node = LeafNode(f"h{head_num}", text_to_textnodes(heading_text))

    return heading_node

def create_code_node(code):

    stripped_code = code.lstrip("```\n")
    stripped_code = stripped_code.rstrip("\n```")

    pre_node = LeafNode("pre", stripped_code)
    code_node = ParentNode("code", pre_node)

    return code_node

def create_quote_node(quote):
        
        split_quote = quote.split("> ")
        full_quote = "".join(split_quote[1:])
        
        quote_node = LeafNode("blockquote", text_to_textnodes(full_quote))

        return quote_node

def create_unordered_list_node(un_list):

    split_list = un_list.split("\n")

    list_items = [] 

    for line in split_list:
        s_line = line.lstrip("* ")
        line_node = LeafNode("li", text_to_textnodes(s_line))
        list_items.append(line_node)

    unordered_list_node = ParentNode("ul", list_items)

    return unordered_list_node

def create_ordered_list_node(or_list):

    split_list = or_list.split("\n")

    list_items = []

    for i in range(0, len(split_list)):
        j = i + 1

        s_line = split_list[i].lstrip(f"{j}. ")
        line_node = LeafNode("li", text_to_textnodes(s_line))
        list_items.append(line_node)

    ordered_list_node = ParentNode("ol", list_items)

    return ordered_list_node

def create_paragraph_node(paragraph):

    paragraph_node = LeafNode("p", text_to_textnodes(paragraph))

    return paragraph_node
