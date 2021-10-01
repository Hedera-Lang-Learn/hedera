from collections import namedtuple

from lemmatization.services.chinese import ChineseService, LACChineseTokenizer
from lemmatization.services.greek import GreekService, GreekTokenizer
from lemmatization.services.latin import EncliticTokenizer, LatinService
from lemmatization.services.russian import ClancyService, RUSTokenizer


# using ISO 639.2 CODES

SupportedLanguage = namedtuple("SupportedLanguage", ["code", "verbose_name", "service", "tokenizer"])


SUPPORTED_LANGUAGES = {
    "grc": SupportedLanguage("grc", "Ancient Greek", GreekService(lang="grc"), GreekTokenizer(lang="grc")),
    "lat": SupportedLanguage("lat", "Latin", LatinService(lang="lat"), EncliticTokenizer(lang="lat")),
    "rus": SupportedLanguage("rus", "Russian", ClancyService(lang="rus"), RUSTokenizer(lang="rus")),
    "zho": SupportedLanguage("zho", "Chinese", ChineseService(lang="zho"), LACChineseTokenizer(lang="zho"))
}
