from collections import namedtuple

# from lemmatization.services.chinese import ChineseService, LACChineseTokenizer
# from lemmatization.services.greek import GreekService, GreekTokenizer
from lemmatization.services.latin import EncliticTokenizer, LatinService


# from lemmatization.services.russian import ClancyService, RUSTokenizer
=======
from lemmatization.services.chinese import (
    ChinesePreprocessor,
    ChineseService,
    LACChineseTokenizer
)
from lemmatization.services.greek import (
    GreekPreprocessor,
    GreekService,
    GreekTokenizer
)
from lemmatization.services.latin import (
    EncliticTokenizer,
    LatinPreprocessor,
    LatinService
)
from lemmatization.services.russian import (
    ClancyService,
    RUSPreprocessor,
    RUSTokenizer
)


# using ISO 639.2 CODES

SupportedLanguage = namedtuple("SupportedLanguage", ["code", "verbose_name", "service", "tokenizer"])

#NOTE: disables language here for version 1.0
#TODO: Add back languages after
SUPPORTED_LANGUAGES = {
    # "grc": SupportedLanguage("grc", "Ancient Greek", GreekService(lang="grc"), GreekTokenizer(lang="grc")),
    "lat": SupportedLanguage("lat", "Latin", LatinService(lang="lat"), EncliticTokenizer(lang="lat")),
    # "rus": SupportedLanguage("rus", "Russian", ClancyService(lang="rus"), RUSTokenizer(lang="rus")),
    # "zho": SupportedLanguage("zho", "Chinese", ChineseService(lang="zho"), LACChineseTokenizer(lang="zho"))
=======
SupportedLanguage = namedtuple("SupportedLanguage", ["code", "verbose_name", "service", "tokenizer", "preprocessor"])

SUPPORTED_LANGUAGES = {
    "grc": SupportedLanguage("grc", "Ancient Greek", GreekService(lang="grc"), GreekTokenizer(lang="grc"), GreekPreprocessor(lang="grc")),
    "lat": SupportedLanguage("lat", "Latin", LatinService(lang="lat"), EncliticTokenizer(lang="lat"), LatinPreprocessor(lang="lat")),
    "rus": SupportedLanguage("rus", "Russian", ClancyService(lang="rus"), RUSTokenizer(lang="rus"), RUSPreprocessor(lang="rus")),
    "zho": SupportedLanguage("zho", "Chinese", ChineseService(lang="zho"), LACChineseTokenizer(lang="zho"), ChinesePreprocessor(lang="zho"))
}
