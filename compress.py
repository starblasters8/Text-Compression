import sys, os
from typing import List
from decompress import lzw_decompress, test_loss, static_decompress

# Add the static dictionary
static_dictionary = {
    "the": "á",
    "and": "à",
    "for": "ä",
    "are": "ã",
    "but": "å",
    "not": "æ",
    "you": "ç",
    "all": "è",
    "any": "é",
    "can": "ê",
    "her": "ë",
    "was": "ì",
    "one": "í",
    "our": "î",
    "out": "ï",
    "day": "ð",
    "get": "ñ",
    "has": "ò",
    "him": "ó",
    "his": "ô",
    "how": "õ",
    "man": "ö",
    "new": "ø",
    "now": "ù",
    "old": "ú",
    "see": "û",
    "two": "ü",
    "way": "ý",
    "who": "þ",
    "boy": "ÿ",
    "did": "Ā",
    "its": "ā",
    "let": "Ă",
    "put": "ă",
    "say": "Ą",
    "she": "ą",
    "too": "Ć",
    "use": "ć",
    "dad": "Ĉ",
    "mom": "ĉ",
    "that": "Ċ",
    "with": "ċ",
    "from": "Č",
    "they": "č",
    "this": "Ď",
    "have": "ď",
    "more": "Đ",
    "will": "đ",
    "your": "Ē",
    "about": "ē",
    "which": "Ĕ",
    "when": "ĕ",
    "there": "Ė",
    "where": "ė",
    "their": "Ę",
    "would": "ę",
    "these": "Ě",
    "other": "ě",
    "people": "Ĝ",
    "after": "ĝ",
    "first": "Ğ",
    "think": "ğ",
    "great": "Ġ",
    "never": "ġ",
    "little": "Ģ",
    "might": "ģ",
    "should": "Ĥ",
    "could": "ĥ",
    "going": "Ħ",
    "house": "ħ",
    "right": "Ĩ",
    "something": "ĩ",
    "things": "Ī",
    "always": "ī",
    "around": "Ĭ",
    "because": "ĭ",
    "before": "Į",
    "better": "į",
    "different": "İ",
    "friends": "ı",
    "school": "Ĳ",
    "thought": "ĳ",
    "together": "Ĵ",
    "without": "ĵ",
}

# Function to compress the input text using the static dictionary
def static_compress(text: str) -> str:
    compressed_text = text
    for word, code in static_dictionary.items():
        compressed_text = compressed_text.replace(word, code)
    return compressed_text

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

# Function to save the compressed data to a file
def save_compressed_data(filename: str, compressed_data: List[int]) -> None:
    with open(filename, "wb") as f:
        for code in compressed_data:
            f.write(code.to_bytes(2, byteorder="big"))

def check_text(text: str) -> str:
    output = ""
    for char in text:
        if 0 <= ord(char) <= 127:
            output += char
        else:
            print("Error, non unicode character found. Skipping character...")

    return output

def process(file: str, compressed: str, decompressed: str, dev=False, ndigits=4) -> None:
    with open(file, "r") as f:
        text = f.read()

    text = check_text(text)

    compressed_data = lzw_compress(text)

    # Save the compressed data to a file
    save_compressed_data(compressed, compressed_data)

    start = os.path.getsize(file)*8
    end = os.path.getsize(compressed)*8

    print("\nFile: " + file)
    print("Before compression: " + str(start) + " bits")
    print("After compression: " + str(end) + " bits")
    print("Percentage reduced: " + str(round((1-(end/start))*100, ndigits=ndigits)) + "%")

    # Run decompression
    lzw_decompress(compressed, decompressed)

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