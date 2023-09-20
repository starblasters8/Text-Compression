def test_loss(f1: str, f2: str) -> bool:
    with open(f1, "r") as f:
        f1_text = f.read()
    with open(f2, "r") as f:
        f2_text = f.read()
    return f1_text == f2_text