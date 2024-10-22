def test_loss(f1: str, f2: str) -> bool:
    with open(f1, "r") as f:
        f1_text = f.read()
    with open(f2, "r") as f:
        f2_text = f.read()
    return f1_text == f2_text

def check_text(text: str) -> str:
    output = ""
    non_unicode = 0
    for char in text:
        if 0 <= ord(char) <= 127:
            output += char
        else:
            non_unicode += 1
    print(f"\nNon-unicode characters: {non_unicode}")

    return output