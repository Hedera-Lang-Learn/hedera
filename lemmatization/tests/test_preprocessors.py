from django.test import TransactionTestCase

from ..models import FormToLemma, Lemma
from ..services.latin import LatinPreprocessor
from .test_data import test_data_list


class LatinPreprocessorTests(TransactionTestCase):
    def setUp(self):
        for form_data in test_data_list:
            lemma_data = form_data["lemma_data"]
            lemma_qs = Lemma.objects.filter(lang=lemma_data["lang"], lemma=lemma_data["lemma"])
            if not lemma_qs.exists():
                lemma = Lemma.objects.create(**lemma_data)
                FormToLemma.objects.create(lang=form_data["lang"], lemma=lemma, form=form_data["form"])

    def test_successful_word_with_enclitics(self):
        """
        Test word splitting on enclitic based on form exist in `FormtoLemma` table
        """
        input_tokens = [("virumque", "virumque", " ")]
        expected_result = [("virum", "que", ""), ("que", "que", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocessor(input_tokens), expected_result
        )

    def test_word_with_macron_without_enclitics(self):
        """
        Test word with macrons but no enclitics
        """
        input_tokens = [("ratiōne", "ratione", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocessor(input_tokens), input_tokens
        )

    def test_word_without_enclitics(self):
        """
        Test word with no enclitics
        """
        input_tokens = [("sum", "sum", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocessor(input_tokens), input_tokens
        )

    def test_name_without_enclitics(self):
        """
        Test name without any enclitics particles
        """
        input_tokens = [("Medea", "Medea", " ")]
        self.assertEqual(
            LatinPreprocessor(lang="lat").preprocessor(input_tokens), input_tokens
        )
