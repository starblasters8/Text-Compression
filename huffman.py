import os
from collections import defaultdict
from typing import Dict, List, Tuple

class HuffmanNode:
    def __init__(self, char: str, freq: int, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

def build_frequency_table(text: str) -> Dict[str, int]:
    freq_table = defaultdict(int)
    for char in text:
        freq_table[char] += 1
    return freq_table

def build_huffman_tree(freq_table: Dict[str, int]) -> HuffmanNode:
    nodes = [HuffmanNode(char, freq) for char, freq in freq_table.items()]

    while len(nodes) > 1:
        nodes.sort(key=lambda node: node.freq)

        left = nodes.pop(0)
        right = nodes.pop(0)

        new_node = HuffmanNode(None, left.freq + right.freq, left, right)
        nodes.append(new_node)

    return nodes[0]

def build_huffman_codes(tree: HuffmanNode, prefix: str = "") -> Dict[str, str]:
    if tree.is_leaf():
        return {tree.char: prefix}

    codes = {}
    if tree.left:
        codes.update(build_huffman_codes(tree.left, prefix + "0"))
    if tree.right:
        codes.update(build_huffman_codes(tree.right, prefix + "1"))

    return codes

def huffman_compress(text: str) -> Tuple[str, Dict[str, str]]:
    freq_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    huffman_codes = build_huffman_codes(huffman_tree)

    compressed_text = "".join([huffman_codes[char] for char in text])

    return compressed_text, huffman_codes

def huffman_decompress(compressed_text: str, huffman_codes: Dict[str, str]) -> str:
    reversed_codes = {code: char for char, code in huffman_codes.items()}

    decompressed_text = []
    current_code = ""

    for bit in compressed_text:
        current_code += bit
        if current_code in reversed_codes:
            decompressed_text.append(reversed_codes[current_code])
            current_code = ""

    return "".join(decompressed_text)