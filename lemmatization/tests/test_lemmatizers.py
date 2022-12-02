from django.test import TransactionTestCase

from ..models import FormToLemma, Lemma
from ..services.latin import LatinService


# Chinese language test commented out until support for this language is enabled again.
# class ChineseServiceTests(SimpleTestCase):
#     def test_service(self):
#         """
#         Lemmatization is simple: output is simply a list with the input as the only member;
#         the input is not transformed, nor any additional lemmata included.
#         """
#         text_input = "月"
#         self.assertEqual(
#             ChineseService(lang="zho").lemmatize(text_input),
#             [text_input]
#         )


class LatinServiceTests(TransactionTestCase):
    def test_lemmatize_forms_of_sum(self):
        """
        Lemmatize forms of sum.
        This is not intended to be an exhaustive check on all possible conjugations.
        """

        # Maps each token to one or more lemmas
        token_to_lemmas = {
            # indicative present active forms
            "sum": ["sum"],
            "es": ["sum"],
            "est": ["edo", "sum"],
            "sumus": ["sum"],
            "estis": ["sum"],
            "sunt": ["sum"],

            # indicative future active forms
            "ero": ["aero", "erus", "sum"],
            "eris": ["aero", "erus", "sum"],
            "erit": ["sum"],
            "erimus": ["sum"],
            "eritis": ["sum"],
            "erunt": ["sum"]
        }

        # Add mappings to DB
        for (token, lemmas) in token_to_lemmas.items():
            for lemma in lemmas:
                lemma_object, _ = Lemma.objects.get_or_create(
                    lang="lat",
                    lemma=lemma,
                    alt_lemma=lemma,
                    label=lemma,
                )
                FormToLemma.objects.create(lang="lat", form=token, lemma=lemma_object)

        # Check that they are lemmatized as expected
        service = LatinService(lang="lat")
        for (token, lemmas) in token_to_lemmas.items():
            expected_lemmas_set = set(lemmas)
            actual_lemmas_set = set(service.lemmatize(token, token))
            self.assertEqual(actual_lemmas_set, expected_lemmas_set)
