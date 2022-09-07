from collections import namedtuple

# from lemmatization.services.chinese import (
#     ChinesePreprocessor,
#     ChineseService,
#     LACChineseTokenizer
# )
# from lemmatization.services.greek import (
#     GreekPreprocessor,
#     GreekService,
#     GreekTokenizer
# )
# from lemmatization.services.russian import (
#     ClancyService,
#     RUSPreprocessor,
#     RUSTokenizer
# )
from lemmatization.services.latin import (
    EncliticTokenizer,
    LatinPreprocessor,
    LatinService
)


# using ISO 639.2 CODES
#NOTE: disables language here for version 1.0
#TODO: Add back languages after
SupportedLanguage = namedtuple("SupportedLanguage", ["code", "verbose_name", "service", "tokenizer", "preprocessor"])

SUPPORTED_LANGUAGES = {
    # "grc": SupportedLanguage("grc", "Ancient Greek", GreekService(lang="grc"), GreekTokenizer(lang="grc"), GreekPreprocessor(lang="grc")),
    "lat": SupportedLanguage("lat", "Latin", LatinService(lang="lat"), EncliticTokenizer(lang="lat"), LatinPreprocessor(lang="lat")),
    # "rus": SupportedLanguage("rus", "Russian", ClancyService(lang="rus"), RUSTokenizer(lang="rus"), RUSPreprocessor(lang="rus")),
    # "zho": SupportedLanguage("zho", "Chinese", ChineseService(lang="zho"), LACChineseTokenizer(lang="zho"), ChinesePreprocessor(lang="zho"))
}
