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

dupe_vocab_list_tsv_content = b"""\
quam\thow
quam\thow"""

dupe_headword_list_tsv_content = b"""\
quam\tas possible as
quam\thow
quam\tthan"""

EXAMPLE_VOCAB_LIST_TSV = SimpleUploadedFile("test.tsv", vocab_list_tsv_content)
DUPLICATE_VOCAB_LIST_TSV = SimpleUploadedFile("dupe_test.tsv", dupe_vocab_list_tsv_content)
DUPLICATE_HEADWORD_VOCAB_LIST_TSV = SimpleUploadedFile("dupe_headword_test.tsv", dupe_headword_list_tsv_content)


def create_user(username, email, password):
    return get_user_model().objects.create_user(username, email=email, password=password)


def check_entries(expected_entries, actual_entries):
    bool_list = [
        True
        for expected_entry in expected_entries
        for actual_entry in actual_entries
        if actual_entry.items() >= expected_entry.items()
    ]
    return len(bool_list) == len(expected_entries)


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
            "title": "Foo",
            "description": "Bar",
            "link_status": 0.0,
            "owner": None
        }
        self.assertGreaterEqual(self.vocab_list.data().items(), expected_data.items())

    def test_display_name(self):
        self.assertEqual(self.vocab_list.display_name(), "Latin")

    def test_entry_data(self):
        entry = VocabularyListEntry.objects.filter(vocabulary_list=self.vocab_list)
        expected_data = {
            "headword": "melon",
            "gloss": "armor",
            "node": None
        }
        found = list(filter(lambda vocab_dict: vocab_dict == expected_data, entry.values("headword", "gloss", "node")))
        self.assertGreaterEqual(len(found), 1)

    def test_duplicate_headword_and_gloss_tsv(self):
        dup_headword_vocab_list = VocabularyList(
            lang="lat",
            title="duplicate headwords",
            description="dupes"
        )
        dup_headword_vocab_list.save()
        dup_headword_vocab_list.load_tab_delimited(DUPLICATE_VOCAB_LIST_TSV)
        dup_vocab_list = VocabularyListEntry.objects.filter(vocabulary_list=dup_headword_vocab_list)
        found_match = list(filter(lambda vocab_dict: vocab_dict["headword"] == "quam", dup_vocab_list.values("id", "headword", "gloss")))

        self.assertGreaterEqual(bool(found_match), True)

    def test_duplicate_headword_diff_gloss_tsv(self):
        dup_headword_vocab_list = VocabularyList(
            lang="lat",
            title="duplicate headwords",
            description="dupes"
        )
        dup_headword_vocab_list.save()
        dup_headword_vocab_list.load_tab_delimited(DUPLICATE_HEADWORD_VOCAB_LIST_TSV)
        dup_vocab_list = VocabularyListEntry.objects.filter(vocabulary_list=dup_headword_vocab_list)
        found_match = list(filter(lambda vocab_dict: vocab_dict["headword"] == "quam", dup_vocab_list.values("id", "headword", "gloss")))

        self.assertGreaterEqual(len(found_match), 2)


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
        expected_entries = [
            {
                "headword": "bin",
                "gloss": "bash",
                "familiarity": 2,
            },
            {
                "headword": "foo",
                "gloss": "bar",
                "familiarity": 2,
            },
            {
                "headword": "hello",
                "gloss": "world",
                "familiarity": 2,
            },
            {
                "headword": "melon",
                "gloss": "armor",
                "familiarity": 2,
            }
        ]
        self.assertTrue(check_entries(expected_entries, self.vocab_list.data()["entries"]))

    def test_display_name(self):
        self.assertEqual(self.vocab_list.display_name(), "Latin")

    def test_entry_data(self):
        entry = PersonalVocabularyListEntry.objects.filter(vocabulary_list=self.vocab_list)
        expected_data = {
            "headword": "melon",
            "gloss": "armor",
            "familiarity": 2,
            "node": None
        }
        found = list(filter(lambda vocab_dict: vocab_dict == expected_data, entry.values("headword", "gloss", "familiarity", "node")))
        self.assertGreaterEqual(len(found), 1)

    def test_duplicate_headword_and_gloss_tsv(self):
        user = create_user("donkeykong", "donkeykong@fake.com", "password")
        dup_headword_vocab_list = PersonalVocabularyList(
            lang="lat",
            user=user
        )
        dup_headword_vocab_list.save()
        dup_headword_vocab_list.load_tab_delimited(DUPLICATE_VOCAB_LIST_TSV, 2)
        dup_vocab_list = PersonalVocabularyListEntry.objects.filter(vocabulary_list=dup_headword_vocab_list)
        found_match = list(filter(lambda vocab_dict: vocab_dict["headword"] == "quam", dup_vocab_list.values("id", "headword", "gloss")))

        self.assertGreaterEqual(len(found_match), 1)

    def test_duplicate_headword_diff_gloss_tsv(self):
        user = create_user("diddykong", "diddykong@fake.com", "password")
        dup_headword_vocab_list = PersonalVocabularyList(
            lang="lat",
            user=user
        )
        dup_headword_vocab_list.save()
        dup_headword_vocab_list.load_tab_delimited(DUPLICATE_HEADWORD_VOCAB_LIST_TSV, 2)
        dup_vocab_list = PersonalVocabularyListEntry.objects.filter(vocabulary_list=dup_headword_vocab_list)
        found_match = list(filter(lambda vocab_dict: vocab_dict["headword"] == "quam", dup_vocab_list.values("id", "headword", "gloss")))

        self.assertGreaterEqual(len(found_match), 2)
