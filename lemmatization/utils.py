import unicodedata


def strip_macrons(word):
    return unicodedata.normalize("NFC", "".join(
        ch for ch in unicodedata.normalize("NFD", word) if ch not in ["\u0304"]
    ))
