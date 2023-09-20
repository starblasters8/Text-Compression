import sys, os
from typing import List
from decompress import decompress, test_loss

# Function to compress the input text using LZW algorithm
def compress(text: str) -> List[int]:
    # Initialize the dictionary with ASCII characters
    dictionary = {chr(i): i for i in range(256)}

    result = []
    current_sequence = ""

    # Iterate through the input text
    for char in text:
        # Check if the current sequence with the new character exists in the dictionary
        if current_sequence + char in dictionary:
            # If it exists, update the current sequence
            current_sequence += char
        else:
            # If it doesn't exist, add the current sequence to the result
            result.append(dictionary[current_sequence])

            # Add the new sequence to the dictionary
            dictionary[current_sequence + char] = len(dictionary)

            # Reset the current sequence to the new character
            current_sequence = char

    # Add the last sequence to the result
    if current_sequence:
        result.append(dictionary[current_sequence])

    return result

# Function to save the compressed data to a file
def save_compressed_data(filename: str, compressed_data: List[int]) -> None:
    with open(filename, "wb") as f:
        for code in compressed_data:
            f.write(code.to_bytes(2, byteorder="big"))

def process(file: str, compressed: str, decompressed: str, dev=False) -> None:
    with open(file, "r") as f:
        text = f.read()

    compressed_data = compress(text)

    # Save the compressed data to a file
    save_compressed_data(compressed, compressed_data)

    print("Before compression: " + str(os.path.getsize(file)) + " bytes")
    print("After compression: " + str(os.path.getsize(compressed)) + " bytes")

    # Run decompression
    decompress(compressed, decompressed)

    if dev:
        print("Base and decompressed files are the same: " + str(test_loss(file, decompressed)))


def main():
    if len(sys.argv) == 1:
        file = "test"
    else:
        file = sys.argv[1]

    if file == "test":
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