from django.test import SimpleTestCase

from ..services.chinese import ChineseService


class ChineseServiceTests(SimpleTestCase):
    def test_service(self):
        """
        Lemmatization is simple: output is simply a list with the input as the only member;
        the input is not transformed, nor any additional lemmata included.
        """
        text_input = "月"
        self.assertEqual(
            ChineseService(lang="zho").lemmatize(text_input),
            [text_input]
        )
