import os
import shutil
from time import sleep
from pathlib import Path


from textnode import TextNode, TextType
from leafnode import LeafNode
from copy_to_public import copy_to_public
from generate_page import generate_page

PATH_PREFIX = Path("/home/mike/code/boot.dev/StaticSiteGenerator/Static-Site-Generator/")
STATIC_PATH = PATH_PREFIX.joinpath("static")
PUBLIC_PATH = PATH_PREFIX.joinpath("public")
CONTENT_PATH = PATH_PREFIX.joinpath("content")

def main():
    copy_to_public(STATIC_PATH, PUBLIC_PATH)
    generate_page(
            CONTENT_PATH,
            PATH_PREFIX.joinpath("template.html"),
            PUBLIC_PATH
            )



main()

