import re
import unicodedata

from .base import MorpheusService, Tokenizer, triples


class GreekService(MorpheusService):
    lang = "grc"


class GreekTokenizer(Tokenizer):

    def tokenize(self, text):
        text = unicodedata.normalize("NFC", text)
        tokens = re.split(r"(\W+)", text)
        return triples(tokens)
