import re
import unicodedata

from .base import Tokenizer, triples
from .morpheus import MorpheusService


class GreekService(MorpheusService):
    lang = "grc"


class GreekTokenizer(Tokenizer):

    def tokenize(self, text):
        text = unicodedata.normalize("NFC", text)
        tokens = re.split(r"(\W+)", text)
        return triples(tokens)
