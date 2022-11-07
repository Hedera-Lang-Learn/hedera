from django.test import SimpleTestCase

from ..services.chinese import LACChineseTokenizer
from ..services.latin import LatinTokenizer


class LACChineseTokenizerTests(SimpleTestCase):
    def test_prepare_for_segmentation(self):
        """
        prepare_for_segmentation() strips carriage returns from input (for
        better LAC segmentation)
        """
        input_text = "山\r\n月"
        self.assertEqual(
            LACChineseTokenizer(lang="zho").prepare_for_segmentation(input_text), "山\n月"
        )

    def test_re_tokenize_split_on_newlines(self):
        """
        re_tokenize() splits tokens on new lines (\n)
        - lemma tokens containing "\n" are treated as separate lemmas and the
        "\n" is kept as a distinct non-lemma token
        """
        tokenized_input = [
            "哈哈\n\n",  # newlines should be split from token but retained in token stream
            "\n哈哈",  # newline should be split from token but retained in token stream
            "哈",
            "哈\n哈\n哈",  # newlines should be split from token (and retained), causing token to split into three separate lemma tokens
        ]
        self.assertEqual(
            list(LACChineseTokenizer(lang="zho").re_tokenize(tokenized_input)),
            [
                "哈哈",
                "\n",
                "\n",
                "\n",
                "哈哈",
                "哈",
                "哈",
                "\n",
                "哈",
                "\n",
                "哈",
            ],
        )

    def test_re_tokenize_split_on_pipes(self):
        """
        re_tokenize() splits tokens on pipes (|)
        - lemma tokens containing "|" are treated as separate lemmas and the
        "|" is discarded
        """
        tokenized_input = [
            "華盛頓|郵報",  # should split into two tokens with pipe discarded
            "/",
            "華盛頓",
            "|",  # should be removed, as its two neighbors are already split
            "郵報",
            "|哈|哈|哈|",  # multiples should split this into three tokens,
        ]
        self.assertEqual(
            list(LACChineseTokenizer(lang="zho").re_tokenize(tokenized_input)),
            [
                "華盛頓",
                "郵報",
                "/",
                "華盛頓",
                "郵報",
                "哈",
                "哈",
                "哈",
            ],
        )

    def test_chinese_triples(self):
        """
        get_triples() converts single-token stream into stream of triples:
        - non-lemma tokens preceding first lemma are added as "following"
        to an empty initial token/lemma
        - normalized lemma is simply the original lemma (no normalization)
        - non-lemma tokens such as punctuation and spacing are added as
        "following" to previous lemma
        """
        # pre-tokenized text: `“舉頭望山月， 低頭思故鄉。”`
        tokenized_input = [
            "“",  # (Following)
            "舉頭",  # new token
            "望",  # new token
            "山月",  # new token
            "，",  # (Following)
            " ",  # (Following)
            "低頭",  # new token
            "思",  # new token
            "故鄉",  # new token
            "。",  # (Following)
            "”",  # (Following)
        ]
        triples = list(LACChineseTokenizer(lang="zho").get_triples(tokenized_input))
        self.assertEqual(
            triples,
            [
                ("", "", "“"),
                ("舉頭", "舉頭", ""),
                ("望", "望", ""),
                ("山月", "山月", "， "),
                ("低頭", "低頭", ""),
                ("思", "思", ""),
                ("故鄉", "故鄉", "。”"),
            ],
        )

    def test_get_triples_combining_tokens(self):
        """
        get_triples() converts single-token stream into stream of triples with
        tokens explicitly marked for combining are a single output triple
        - prefixed or suffixed "_" characters cause previous or following
        tokens to join into a single lemma and the "_" is discarded
        """
        # pre-tokenized text: `哈_哈_哈。哈哈哈！`
        tokenized_input = [
            "哈_哈",  # new token
            "_",  # continuation of previous token
            "哈",  # continuation of previous token
            "。",  # (following)
            "哈",  # new token
            "哈_",  # new token
            "哈",  # continuation of previous token
            "！",  # (following)
        ]
        triples = list(LACChineseTokenizer(lang="zho").get_triples(tokenized_input))
        self.assertEqual(
            triples,
            [
                ("哈哈哈", "哈哈哈", "。"),
                ("哈", "哈", ""),
                ("哈哈", "哈哈", "！"),
            ],
        )

    def test_tokenizer(self):
        """
        Chinese text strings are properly segmented and typical punctuation and
        spaces are rendered as 'following' text.
        """
        text_input = "“舉頭望山月， 低頭思故鄉。”"
        output = LACChineseTokenizer(lang="zho").tokenize(text_input)
        self.assertEqual(
            list(output),
            [
                ("", "", "“"),
                ("舉頭", "舉頭", ""),
                ("望", "望", ""),
                ("山月", "山月", "， "),
                ("低頭", "低頭", ""),
                ("思", "思", ""),
                ("故鄉", "故鄉", "。”"),
            ],
        )

    def test_tokenizer_latin_characters(self):
        """
        Latin characters are considered non-lemma characters
        (In practice this means that some mixed-language text will not
        be looked up in the lattice / treated as lemmas, such as
        3Q ("thank you"), 2019冠狀病毒病 ("COVID-19"))
        """
        text_input = "2019冠狀病毒病/3Q/K書"
        output = LACChineseTokenizer(lang="zho").tokenize(text_input)
        self.assertEqual(
            list(output),
            [
                ("", "", "2019"),
                ("冠狀病毒病", "冠狀病毒病", "/3Q/K"),
                ("書", "書", ""),
            ],
        )

    def test_tokenizer_unicode_normalization(self):
        """
        normalize_chinese() normalizes full-width pipe and underscore characters,
        and performs some CJK character normalization
        """
        lac_tokenizer = LACChineseTokenizer(lang="zho")
        # the first character is an alternate form of the second character, but they should not be transformed by NFC
        text_input_no_change = "⺼!=月 / ，!=, / 。!=."
        self.assertEqual(
            lac_tokenizer.normalize_chinese(text_input_no_change),
            text_input_no_change,
        )

        # the first character in each pair is the full-width version, the second is the half-width (ASCII) version
        text_input_full_width_punctuation_should_change = "\uFF5C==| / \uFF3F==_"
        self.assertEqual(
            lac_tokenizer.normalize_chinese(text_input_full_width_punctuation_should_change),
            # this is the same string, only with full-width converted to half-width
            "|==| / _==_",
        )

        # the first character is the CJK Compatibility Ideograph \uF9D1, the second is the canonical Unified Ideograph \u516D
        text_input_compatibility_change = "六==六"
        self.assertEqual(
            lac_tokenizer.normalize_chinese(text_input_compatibility_change),
            # this is the same string, only with compatibility chars transformed to canonical
            "六==六",
        )

        # the first character is the non-breaking space character in 4-digit unicode representation
        text_input_compatibility_change = "\u00a0=> "
        self.assertEqual(
            lac_tokenizer.normalize_chinese(text_input_compatibility_change),
            # non-breaking space is removed by normalization
            " => ",
        )

        # the first character is the non-breaking space character in hex representation
        text_input_compatibility_change = "\xa0=> "
        self.assertEqual(
            lac_tokenizer.normalize_chinese(text_input_compatibility_change),
            # non-breaking space is removed by normalization
            " => ",
        )


class LatinTokenizerTests(SimpleTestCase):
    def test_tokenizer_text_no_macrons(self):
        text_input = "Medea, filia regis, amorem ratione vincere conatur."
        output = list(LatinTokenizer(lang="lat").tokenize(text_input))
        self.assertEqual(output, [
            ("Medea", "Medea", ", "),
            ("filia", "filia", " "),
            ("regis", "regis", ", "),
            ("amorem", "amorem", " "),
            ("ratione", "ratione", " "),
            ("vincere", "vincere", " "),
            ("conatur", "conatur", "."),
            ("", "", " "),
        ])

    def test_tokenizer_text_with_macrons(self):
        text_input = "Medea, fīlia rēgis, amōrem ratiōne vincere conātur."
        output = list(LatinTokenizer(lang="lat").tokenize(text_input))
        self.assertEqual(output, [
            ("Medea", "Medea", ", "),
            ("fīlia", "filia", " "),
            ("rēgis", "regis", ", "),
            ("amōrem", "amorem", " "),
            ("ratiōne", "ratione", " "),
            ("vincere", "vincere", " "),
            ("conātur", "conatur", "."),
            ("", "", " "),
        ])

    def test_tokenizer_does_not_auto_split_enclitics(self):
        """
        Enclitics are NOT automatically split off by the tokenizer.

        To handle enclitics (particles hanging on to words like -que),
        either use the pipe (|) to instruct the tokenizer to split it off,
        or rely on the automatic enclitic handling that happens later in the
        lemmatization process (e.g. preprocessing).
        """
        text_input = "estne"
        output = list(LatinTokenizer(lang="lat").tokenize(text_input))
        self.assertEqual(output, [
            ("estne", "estne", " ")
        ])

    def test_tokenizer_pipe_splits_word(self):
        """
        Use the pipe (|) to intsruct the tokenizer that there is a word boundary
        within a word (e.g. to split off an enclitic like -ne or -que).
        """
        text_input = "est|ne"
        output = list(LatinTokenizer(lang="lat").tokenize(text_input))
        self.assertEqual(output, [
            ("est", "est", ""),
            ("ne", "ne", " "),
        ])

    def test_tokenizer_underscore_combines_words_with_latin_copula(self):
        """
        Use the underscore (_) to combine words that should be represented as a
        single unit of meaning. This is often used with latin copula, or connective/linking
        words. In that case, we expect the linking word (latin copula) to be removed in
        the normalized representation of the word.
        """
        text_input = "expulsus_est"
        output = list(LatinTokenizer(lang="lat").tokenize(text_input))
        self.assertEqual(output, [
            # the normalized word has any words in the latin copula removed
            # automatically, since these are considered connecting words
            ("expulsus est", "expulsus", " "),
        ])
