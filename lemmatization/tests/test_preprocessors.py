from django.test import TestCase

from ..models import FormToLemma, Lemma
from ..services.latin import LatinPreprocessor
from .test_data import test_data_list


class LatinPreprocessorTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Setup test data for the whole TestCase.
        """
        for form_data in test_data_list:
            lang = form_data["lang"]
            form = form_data["form"]
            lemma = form_data["lemma_data"]["lemma"]
            lemma_object, created = Lemma.objects.get_or_create(lang=lang, lemma=lemma)
            FormToLemma.objects.create(lang=lang, form=form, lemma=lemma_object)

    def test_successful_word_with_enclitics(self):
        """
        Test word splitting on enclitic based on form exist in `FormtoLemma` table
        """
        tests = [
            {
                "input_tokens": [("virumque", "virumque", " ")],
                "expected_result": [("virum", "virum", ""), ("que", "que", " ")]
            },
            {
                "input_tokens": [("estne", "estne", " ")],
                "expected_result": [("est", "est", ""), ("ne", "ne", " ")]
            },
        ]

        for test in tests:
            self.assertEqual(
                LatinPreprocessor(lang="lat").preprocess(test["input_tokens"]),
                test["expected_result"]
            )

    def test_word_with_enclitic_but_unknown(self):
        """
        Test word with enclitic, but preceding word is unknown so it's not split off.
        """
        input_tokens = [("somethingque", "somethingque", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocess(input_tokens), input_tokens
        )

    def test_word_ending_with_enclitic_twice(self):
        """
        Test a word that naturally ends in -ne like "arachne" AND has the -ne enclitic on the end.
        This should test an edge case where the enclitic appears twice in the string.
        """
        input_tokens = [("arachnene", "arachnene", " ")]
        expected_result = [("arachne", "arachne", ""), ("ne", "ne", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocess(input_tokens), expected_result
        )

    def test_word_with_macron_without_enclitics(self):
        """
        Test word with macrons but no enclitics
        """
        input_tokens = [("ratiōne", "ratione", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocess(input_tokens), input_tokens
        )

    def test_word_without_enclitics(self):
        """
        Test word with no enclitics
        """
        input_tokens = [("sum", "sum", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocess(input_tokens), input_tokens
        )

    def test_name_without_enclitics(self):
        """
        Test name without any enclitics particles
        """
        input_tokens = [("Medea", "Medea", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocess(input_tokens), input_tokens
        )
