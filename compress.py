import sys, os
from typing import List, Dict, Tuple
from compression_utils import check_text, test_loss
from lzw import lzw_compress, lzw_decompress
from huffman import huffman_compress, huffman_decompress

# Function to save the compressed data to a file
def save_compressed_data(filename: str, compressed_data: List[int]) -> None:
    with open(filename, "wb") as f:
        for code in compressed_data:
            f.write(code.to_bytes(2, byteorder="big"))

# Function to load the compressed data from a file
def load_compressed_data(filename: str) -> List[int]:
    compressed_data = []
    with open(filename, "rb") as f:
        while True:
            code = f.read(2)
            if not code:
                break
            compressed_data.append(int.from_bytes(code, byteorder="big"))
    return compressed_data

def decompress(file: str, output: str, compression_type: str="lzw") -> None:
    # Load the compressed data from a file
    compressed_data = load_compressed_data(file)

    # Decompress the input data
    if compression_type == "lzw":
        decompressed_text = lzw_decompress(compressed_data)

    # Save the decompressed text to a file
    with open(output, "w") as f:
        f.write(decompressed_text)

def save_huffman_data(filename: str, compressed_data: str, huffman_codes: Dict[str, str]) -> None:
    with open(filename, "wb") as f:
        # Save the number of Huffman codes
        f.write(len(huffman_codes).to_bytes(2, byteorder="big"))

        # Save the Huffman codes
        for char, code in huffman_codes.items():
            f.write(ord(char).to_bytes(1, byteorder="big"))
            f.write(len(code).to_bytes(1, byteorder="big"))
            f.write(int(code, 2).to_bytes((len(code) + 7) // 8, byteorder="big"))

        # Save the compressed data
        for i in range(0, len(compressed_data), 8):
            byte = compressed_data[i:i + 8]
            f.write(int(byte, 2).to_bytes((len(byte) + 7) // 8, byteorder="big"))

def load_huffman_data(filename: str) -> Tuple[str, Dict[str, str]]:
    compressed_data = ""
    huffman_codes = {}

    with open(filename, "rb") as f:
        # Load the number of Huffman codes
        num_codes = int.from_bytes(f.read(2), byteorder="big")

        # Load the Huffman codes
        for _ in range(num_codes):
            char = chr(int.from_bytes(f.read(1), byteorder="big"))
            code_length = int.from_bytes(f.read(1), byteorder="big")
            code = format(int.from_bytes(f.read((code_length + 7) // 8), byteorder="big"), f"0{code_length}b")
            huffman_codes[char] = code

        # Load the compressed data
        while True:
            byte = f.read(1)
            if not byte:
                break
            compressed_data += format(int.from_bytes(byte, byteorder="big"), "08b")

    return compressed_data, huffman_codes

def decompress_huffman(file: str, output: str) -> None:
    compressed_data, huffman_codes = load_huffman_data(file)
    decompressed_text = huffman_decompress(compressed_data, huffman_codes)

    with open(output, "w") as f:
        f.write(decompressed_text)

def process(file: str, compressed: str, decompressed: str, dev=False, ndigits=4) -> None:
    # Create temp directory if it doesn't exist
    if not os.path.exists("temp"):
        os.makedirs("temp")

    with open(file, "r", encoding='utf-8', errors='replace') as f:
        text = f.read()

    text = check_text(text)
    start = os.path.getsize(file) * 8

    # LZW compression
    compressed_data_lzw = lzw_compress(text)
    save_compressed_data("temp/lzw.zach", compressed_data_lzw)
    lzw_size = os.path.getsize("temp/lzw.zach") * 8

    # Huffman compression
    compressed_data_huffman, huffman_codes = huffman_compress(text)
    save_huffman_data("temp/huffman.zach", compressed_data_huffman, huffman_codes)
    huffman_size = os.path.getsize("temp/huffman.zach") * 8

    # Choose the smaller compressed file
    if lzw_size < huffman_size:
        os.rename("temp/lzw.zach", compressed)
        os.remove("temp/huffman.zach")
        compression_type = "lzw"
        compressed_size = lzw_size
    else:
        os.rename("temp/huffman.zach", compressed)
        os.remove("temp/lzw.zach")
        compression_type = "huffman"
        compressed_size = huffman_size

    end = compressed_size

    print("File: " + file)
    print("Before compression: " + str(start) + " bits")
    print("After compression: " + str(end) + " bits")
    print("Percentage reduced: " + str(round((1 - (end / start)) * 100, ndigits=ndigits)) + "%")
    print("Compression type used: " + compression_type)
    print("Huffman percentage reduced: " + str(round((1 - (huffman_size / start)) * 100, ndigits=ndigits)) + "% Raw size: " + str(huffman_size) + " bits")
    print("LZW percentage reduced: " + str(round((1 - (lzw_size / start)) * 100, ndigits=ndigits)) + "% Raw size: " + str(lzw_size) + " bits")

    # Run decompression
    if compression_type == "lzw":
        decompress(compressed, decompressed, "lzw")
    elif compression_type == "huffman":
        decompress_huffman(compressed, decompressed)

    if dev:
        print("Base and decompressed files are the same: " + str(test_loss(file, decompressed)))

    # Remove temp directory
    os.rmdir("temp")

def main():
    if len(sys.argv) == 1:
        file = "test"
    else:
        file = sys.argv[1]

    if file == "test":
        # delete all files in test/compressed and test/decompressed
        files = os.listdir("test/compressed")
        for file in files:
            os.remove(f"test/compressed/{file}")
        files = os.listdir("test/decompressed")
        for file in files:
            os.remove(f"test/decompressed/{file}")

        files = os.listdir("test/base")
        for file in files:
            if file.endswith(".txt"):
                process(f"test/base/{file}", f"test/compressed/{file[:-4]}.zach", f"test/decompressed/{file}", True)

    elif file.endswith(".txt"):
        name = file.rsplit("/", 1)
        if len(name) == 1:
            name = ["", name[0]]
        process(file, f"{name[0]}compressed_{name[1].replace('.txt', '.zach')}", f"{name[0]}decompressed_{name[1]}")
    

if __name__ == "__main__":
    main()