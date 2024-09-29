from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from constants import *

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

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0: raise Exception("Unclosed delimiter")

        node_list = []
        oscillator = text_type_text

        for text in split_text:
            node_list.append(TextNode(text, oscillator))
            if oscillator == text_type_text: oscillator = text_type
            else: oscillator = text_type_text

        if node_list[0].text == "": 
            del node_list[0]   
                
        if node_list[-1].text == "":
            del node_list[-1]

        new_node_list.extend(node_list)


    return new_node_list
