from re import findall
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph block"
    HEADING = "heading block"
    CODE = "code block"
    QUOTE = "quote block"
    UNORDERED_LIST = "unordered list block"
    ORDERED_LIST = "ordered list block"

def blocks_to_blocktype(block: str) -> BlockType:
    block = block.strip()

    match block[0]:
        case "#":
            heading_regex = r"^#{1,6} "
            if findall(heading_regex, block):
                return BlockType.HEADING

        case "`":
            if block.startswith("```\n") and block.endswith("```"):
                return BlockType.CODE

        case ">":
            lines = block.split("\n")
            if all(l.startswith(">") for l in lines):
                return BlockType.QUOTE

        case "-":
            lines = block.split("\n")
            if all(l.startswith("- ") for l in lines):
                return BlockType.UNORDERED_LIST

        case "1":
            lines = block.split("\n")
            for number in range(1, len(lines) + 1):
                line = lines[number - 1]
                if not line.startswith(f"{number}. "):
                    break
            else:
                return BlockType.ORDERED_LIST
                    


    return BlockType.PARAGRAPH
    
    
def markdown_to_blocks(markdown: str) -> [str]:
    return [block.strip("\n") for block in markdown.split("\n\n") if block]
