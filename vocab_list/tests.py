from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django.contrib.auth import get_user_model

from .models import (
    PersonalVocabularyList,
    PersonalVocabularyListEntry,
    VocabularyList,
    VocabularyListEntry
)


vocab_list_tsv_content = b"""\
melon\tarmor
foo\tbar
bin\tbash
hello\tworld"""


EXAMPLE_VOCAB_LIST_TSV = SimpleUploadedFile("test.tsv", vocab_list_tsv_content)


def create_user(username, email, password):
    return get_user_model().objects.create_user(username, email=email, password=password)


class VocabularyListAndEntryTests(TestCase):

    def setUp(self):
        self.vocab_list = VocabularyList(
            lang="lat",
            title="Foo",
            description="Bar"
        )
        self.vocab_list.save()
        self.vocab_list.load_tab_delimited(EXAMPLE_VOCAB_LIST_TSV)

    def test_load_tab_delimited(self):
        self.assertEqual(self.vocab_list.entries.count(), 4)

    def test_data(self):
        expected_data = {
            "id": 1,
            "title": "Foo",
            "description": "Bar",
            "link_status": 0.0,
            "owner": None
        }
        self.assertEqual(self.vocab_list.data(), expected_data)

    def test_display_name(self):
        self.assertEqual(self.vocab_list.display_name(), "Latin")

    def test_entry_data(self):
        entry = VocabularyListEntry.objects.filter(vocabulary_list=self.vocab_list).first()
        expected_data = {
            "id": 9,
            "headword": "melon",
            "gloss": "armor",
            "node": None
        }
        self.assertEqual(entry.data(), expected_data)


class PersonalVocabularyListAndEntryTests(TestCase):

    def setUp(self):
        self.user = create_user("okieDokey", "smokey@fake.com", "password")
        self.vocab_list = PersonalVocabularyList(
            lang="lat",
            user=self.user
        )
        self.vocab_list.save()
        self.vocab_list.load_tab_delimited(EXAMPLE_VOCAB_LIST_TSV, 2)

    def test_load_tab_delimited(self):
        self.assertEqual(self.vocab_list.entries.count(), 4)

    def test_data(self):
        expected_data = {
            "entries": [
                {
                    "id": 3,
                    "headword": "bin",
                    "gloss": "bash",
                    "familiarity": 2,
                    "node": None
                },
                {
                    "id": 2,
                    "headword": "foo",
                    "gloss": "bar",
                    "familiarity": 2,
                    "node": None
                },
                {
                    "id": 4,
                    "headword": "hello",
                    "gloss": "world",
                    "familiarity": 2,
                    "node": None
                },
                {
                    "id": 1,
                    "headword": "melon",
                    "gloss": "armor",
                    "familiarity": 2,
                    "node": None
                }
            ],
            "statsByText": {},
            "id": 1
        }
        self.assertEqual(self.vocab_list.data(), expected_data)

    def test_display_name(self):
        self.assertEqual(self.vocab_list.display_name(), "Latin")

    def test_entry_data(self):
        entry = PersonalVocabularyListEntry.objects.filter(vocabulary_list=self.vocab_list).first()
        expected_data = {
            "id": 9,
            "headword": "melon",
            "gloss": "armor",
            "familiarity": 2,
            "node": None
        }
        self.assertEqual(entry.data(), expected_data)
