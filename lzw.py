from typing import List

# Function to compress the input text using LZW algorithm
def lzw_compress(text: str) -> List[int]:
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