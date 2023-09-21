from typing import List

# Function to decompress the input data using LZW algorithm
def lzw_decompress(compressed_data: List[int]) -> str:
    # Initialize the dictionary with ASCII characters
    dictionary = {i: chr(i) for i in range(256)}

    # Initialize variables
    result = []
    current_sequence = dictionary[compressed_data[0]]
    result.append(current_sequence)

    # Iterate through the compressed data
    for code in compressed_data[1:]:
        # Check if the code exists in the dictionary
        if code in dictionary:
            # If it exists, get the corresponding sequence
            new_sequence = dictionary[code]
        else:
            # If it doesn't exist, create a new sequence
            new_sequence = current_sequence + current_sequence[0]

        # Add the new sequence to the result
        result.append(new_sequence)

        # Update the dictionary with the new sequence
        dictionary[len(dictionary)] = current_sequence + new_sequence[0]

        # Update the current sequence
        current_sequence = new_sequence

    return "".join(result)

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

def decompress(file: str, output: str) -> None:
    # Load the compressed data from a file
    compressed_data = load_compressed_data(file)

    # Decompress the input data
    decompressed_text = lzw_decompress(compressed_data)

    # Save the decompressed text to a file
    with open(output, "w") as f:
        f.write(decompressed_text)

def test_loss(f1: str, f2: str) -> bool:
    with open(f1, "r") as f:
        f1_text = f.read()
    with open(f2, "r") as f:
        f2_text = f.read()
    return f1_text == f2_text