import re
import unicodedata
from typing import (  # can use `list` and `tuple` in python 3.9
    Iterable,
    List,
    Tuple
)

from LAC import LAC

from .base import Service, Tokenizer


TripleIterable = Iterable[Tuple[str, str, str]]


class ChineseService(Service):
    """
    Lemmatizer Service for Chinese (zho) text, both simplified and traditional forms.
    """

    SID = "chinese"  # for both simplified and traditional forms
    LANGUAGES = ["zho"]

    def lemmatize(self, form: str) -> List[str]:
        """
        Lemmatized forms are just the words themselves, assuming they've been
        tokenized by a Chinese segmentation parser.
        """
        return [form]


class ChineseTokenizer(Tokenizer):
    """
    Tokenizer for Mandarin Chinese (Zhongwen).
    """
    # this captures a wide swath of Chinese characters and related symbols, such as
    # the Chinese "zero" (〇 or \u3007) and middle dot (· or \u00B7, used with names)
    # without capturing common punctuation (e.g. in the \u3000-303F range)
    # cf https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
    CHINESE_RE = re.compile(
        r"^[\u00B7-\u00B7\u3007-\u3007\u3400-\u4DBF\u4E00-\u9FEF\U00020000-\U0002EBFF]+$"
    )

    def tokenize(self, text: str) -> TripleIterable:
        """
        Tokenize using a standard python Chinese parser.
        """
        # 1. normalize text stream (convert some equivalent
        # characters to their standard forms)
        unicode_normalized_text = self.normalize_chinese(text)

        # 2. perform any text transforms to ensure high-quality
        # segmentation
        prepared_text = self.prepare_for_segmentation(unicode_normalized_text)

        # 3. perform Chinese segmentation
        tokens = self.tokenize_chinese_text(prepared_text)

        # 4. Apply post-processing to the token stream to ensure
        # that lattice lookups will be optimal
        tokens = self.re_tokenize(tokens)

        # 5. Generate stream of lemmatized tokens
        lemma_triples = self.get_triples(tokens)

        return lemma_triples

    def normalize_chinese(self, text: str) -> str:
        """
        Performs Unicode normalization on text. cf Unicode Standard section 2.12.
        Uses NFC (Normalization Form C).

        Also:
        - selectively converts full-width pipe (｜ \uFF5C) and underscore (＿ \uFF3F)
        to half-width (ASCII) | \u007C and _ \u005F (so they can be used to give token
        boundary hints).
        - converts non-breaking spaces (which are sometimes present after editing an
        existing text, due to the UI component employed) into regular spaces (\u00a0
        to \u0020); the typesetting information is lost, but we don't need it for our
        purposes, and it can complicate tokenization.

        >>> # note that the bar and underscore character in the following line are full-width:
        >>> normalize_chinese("1｜2＿3\u00a04\xa05")
        "1|2_3 4 5"

        Note that we use NFC because there are some issues with using NFKC, e.g.:
        - common full-width forms like Chinese commas are transformed into half-width using NFKC
        (and other full-width forms like the pipe/vertical bar are not transformed).
        """
        normalized_text = unicodedata.normalize("NFC", text)  # normalize
        return normalized_text.replace("\uFF5C", "|").replace("\uFF3F", "_").replace("\u00a0", " ")

    def prepare_for_segmentation(self, text: str) -> str:
        """ Override this method """
        raise NotImplementedError

    def tokenize_chinese_text(self, text: str) -> Iterable[str]:
        """ Override this method """
        raise NotImplementedError

    def get_triples(self, tokens: Iterable[str]) -> TripleIterable:
        """
        Converts single-token stream into stream of triples of form
        (lemma, normalized lemma, following). Underscores at token boundaries
        are used to combine separate input tokens into a single output token
        in the stream. Non-Chinese tokens are considered "following" text of
        the previous Chinese (lemma) token.

        >>> get_triples(["/", "舉_", "頭", "望", "山", "_月", "/"])
        [("", "", "/"), ("舉頭", "舉頭", ""), ("望", "望", ""), ("山月", "山月", "/")]
        """
        current_token = ""
        following = ""
        should_extend_current_token = False

        for token in tokens:

            # 1. does the current `token` need to extend the last one because
            #    it _starts_ with an underscore hint?
            if token.startswith("_"):
                # add to previous current_token no matter what, even if it doesn't
                # match the CHINESE_RE
                current_token += token.replace("_", "")
                if token.endswith("_"):
                    # underscore is an explicit hint that this should not be
                    # considered a token boundary, so indicate that the next
                    # `token` should be combined with `current_token`
                    should_extend_current_token = True
                continue

            # 2. does the current `token` need to extend the last one because
            #    the last token _ended_ with an underscore hint?
            if should_extend_current_token:
                # previous `token` indicated that this `token` should be
                # combined with `current_token`; now check whether this `token`
                # indicates next `token` should also be an extension of the
                # `current_token`
                should_extend_current_token = token.endswith("_")
                current_token += token.replace("_", "")
                continue

            # 3. does the current `token` need to signal to the next one
            #    that it should be combined with the `current_token`?
            should_extend_current_token = token.endswith("_")

            # 4. we've got all the information we need from the underscore hint,
            #    so we can safely remove it from the displayed output.
            token = token.replace("_", "")

            # 5. is the current `token` comprised of valid lemma characters?
            if self.CHINESE_RE.match(token):
                # we've reached a lemma token boundary, so is there anything
                # to emit from earlier in the token stream?
                # - note that the preceding tokens may have been valid lemma
                # tokens, in which case they're tracked in `current_token`, or
                # they might have been added to `following` without any valid
                # text in `current_token` yet, e.g. if punctuation like a quote
                # precedes the first valid lemma
                if current_token or following:
                    # emit the currently captured  as a lemma along with any
                    # non-lemma `following` string
                    yield (current_token, self.normalize_token(current_token), following)

                # start new `current_token` string with this valid `token`
                current_token = token
                following = ""
            else:
                # this token is not a valid lemma character, so add it to the
                # `following` text.
                following += token

        # if there's any final token output to add to the output stream now that
        # the input stream is exhausted, do so
        if current_token or following:
            yield (current_token, self.normalize_token(current_token), following)

    def normalize_token(self, token: str) -> str:
        """
        Perform transformations or adjustments to individual Chinese tokens
        """
        return token

    def re_tokenize(self, tokens: Iterable[str]) -> Iterable[str]:
        """ Override this method """
        raise NotImplementedError


class LACChineseTokenizer(ChineseTokenizer):
    """
    Tokenizer for Mandarin Chinese (Zhongwen).
    """
    lac = LAC(mode="seg")

    def prepare_for_segmentation(self, text: str) -> str:
        """
        Perform any processing steps required to optimize string of text for LAC segmentation.
        """
        # LAC seems to work better with just \n delimiters, so remove any \r (e.g. in \r\n sequences)
        return text.replace("\r", "")

    def tokenize_chinese_text(self, text: str) -> Iterable[str]:
        return self.lac.run(text)

    def re_tokenize(self, tokens: Iterable[str]) -> Iterable[str]:
        """
        Ensure any tokens containing pipe hints are split, and that newlines are also split into
        their own tokens, in order to help with lattice lookups downstream. (LAC sometimes includes
        newlines in lemma tokens instead of splitting them out.)

        >>> re_tokenize(["a|b", "c\nd"])
        ["a", "b", "c", "\n", "d"]
        """
        for token in tokens:
            # collect all characters in the token but split on the pipe character, spaces, and newlines
            subtoken = ""
            for char in token:
                # consider pipes, spaces, and newlines to be token breaks; in practice, LAC doesn't always do this
                if char in ("|", " ", "\n"):
                    if subtoken:
                        yield subtoken
                        subtoken = ""
                    # if it is a space or newline, emit it as a separate token; if a pipe, do not emit it
                    if char != "|":
                        yield char
                else:
                    subtoken += char
            if subtoken:
                yield subtoken
