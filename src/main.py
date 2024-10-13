from textnode import TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import functionlibrary as functions
from constants import *
from os import path, listdir, mkdir
from shutil import copy, rmtree

def copy_paths(current_path):
    
    strip_path = current_path.lstrip("static")
    copy_path = "public" + strip_path

    if path.isdir(current_path):
        if not path.exists(copy_path):
            mkdir(copy_path)
        
        for item in listdir(current_path):
            copy_paths(path.join(current_path, item))

    if path.isfile(current_path) and not path.exists(copy_path):
       copy(current_path, copy_path)
    
def copy_static():

    if path.exists("public"):
        rmtree("public")

    copy_paths("static")

    
def main():

    copy_static()

main()

