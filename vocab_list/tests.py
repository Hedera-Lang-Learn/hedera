from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django.contrib.auth import get_user_model

from .models import (
    PersonalVocabularyList,
    PersonalVocabularyListEntry,
    VocabularyList,
    VocabularyListEntry
)


vocab_list_tsv_content = (
    b"headword\tdefinition\n"
    b"melon\tarmor\n"
    b"foo\tbar\n"
    b"bin\tbash\n"
    b"hello\tworld\n"
)

dupe_vocab_list_tsv_content = b"""\
headword\tdefinition
quam\thow
quam\thow"""

dupe_headword_list_tsv_content = b"""\
headword\tdefinition
quam\tas possible as
quam\thow
quam\tthan"""


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
        example_vocab_list_file = SimpleUploadedFile("test.tsv", vocab_list_tsv_content)

        self.vocab_list = VocabularyList(
            lang="lat",
            title="Foo",
            description="Bar"
        )
        self.vocab_list.save()
        self.vocab_list.load_tab_delimited(example_vocab_list_file)

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
            "definition": "armor",
            "lemma": None
        }
        found = list(filter(lambda vocab_dict: vocab_dict == expected_data, entry.values("headword", "definition", "lemma")))
        self.assertEqual(len(found), 1)

    def test_duplicate_headword_and_definition_tsv(self):
        dup_test_file = SimpleUploadedFile("dupe_test.tsv", dupe_vocab_list_tsv_content)
        dup_headword_vocab_list = VocabularyList(
            lang="lat",
            title="duplicate headwords",
            description="dupes"
        )
        dup_headword_vocab_list.save()
        dup_headword_vocab_list.load_tab_delimited(dup_test_file)
        dup_vocab_list = VocabularyListEntry.objects.filter(vocabulary_list=dup_headword_vocab_list)
        found_match = list(filter(lambda vocab_dict: vocab_dict["headword"] == "quam", dup_vocab_list.values("id", "headword", "definition")))

        self.assertEqual(len(found_match), 1)

    def test_duplicate_headword_diff_definition_tsv(self):
        dup_headword_test_file = SimpleUploadedFile("dupe_headword_test.tsv", dupe_headword_list_tsv_content)
        dup_headword_vocab_list = VocabularyList(
            lang="lat",
            title="duplicate headwords",
            description="dupes"
        )
        dup_headword_vocab_list.save()
        dup_headword_vocab_list.load_tab_delimited(dup_headword_test_file)
        dup_vocab_list = VocabularyListEntry.objects.filter(vocabulary_list=dup_headword_vocab_list)
        found_match = list(filter(lambda vocab_dict: vocab_dict["headword"] == "quam", dup_vocab_list.values("id", "headword", "definition")))

        self.assertEqual(len(found_match), 3)


class PersonalVocabularyListAndEntryTests(TestCase):

    def setUp(self):
        example_vocab_list_file = SimpleUploadedFile("test.tsv", vocab_list_tsv_content)

        self.user = create_user("okieDokey", "smokey@fake.com", "password")
        self.vocab_list = PersonalVocabularyList(
            lang="lat",
            user=self.user
        )
        self.vocab_list.save()
        self.vocab_list.load_tab_delimited(example_vocab_list_file, 2)

    def test_load_tab_delimited(self):
        self.assertEqual(self.vocab_list.entries.count(), 4)

    def test_data(self):
        expected_entries = [
            {
                "headword": "bin",
                "definition": "bash",
                "familiarity": 2,
            },
            {
                "headword": "foo",
                "definition": "bar",
                "familiarity": 2,
            },
            {
                "headword": "hello",
                "definition": "world",
                "familiarity": 2,
            },
            {
                "headword": "melon",
                "definition": "armor",
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
            "definition": "armor",
            "familiarity": 2,
            "lemma": None
        }
        found = list(filter(lambda vocab_dict: vocab_dict == expected_data, entry.values("headword", "definition", "familiarity", "lemma")))
        self.assertEqual(len(found), 1)

    def test_duplicate_headword_and_definition_tsv(self):
        dup_test_file = SimpleUploadedFile("dupe_test.tsv", dupe_vocab_list_tsv_content)
        user = create_user("donkeykong", "donkeykong@fake.com", "password")
        dup_headword_vocab_list = PersonalVocabularyList(
            lang="lat",
            user=user
        )
        dup_headword_vocab_list.save()
        dup_headword_vocab_list.load_tab_delimited(dup_test_file, 2)
        dup_vocab_list = PersonalVocabularyListEntry.objects.filter(vocabulary_list=dup_headword_vocab_list)
        found_match = list(filter(lambda vocab_dict: vocab_dict["headword"] == "quam", dup_vocab_list.values("id", "headword", "definition")))

        self.assertEqual(len(found_match), 1)

    def test_duplicate_headword_diff_definition_tsv(self):
        dup_headword_test_file = SimpleUploadedFile("dupe_headword_test.tsv", dupe_headword_list_tsv_content)
        user = create_user("diddykong", "diddykong@fake.com", "password")
        dup_headword_vocab_list = PersonalVocabularyList(
            lang="lat",
            user=user
        )
        dup_headword_vocab_list.save()
        dup_headword_vocab_list.load_tab_delimited(dup_headword_test_file, 2)
        dup_vocab_list = PersonalVocabularyListEntry.objects.filter(vocabulary_list=dup_headword_vocab_list)
        found_match = list(filter(lambda vocab_dict: vocab_dict["headword"] == "quam", dup_vocab_list.values("id", "headword", "definition")))
        self.assertEqual(len(found_match), 3)
