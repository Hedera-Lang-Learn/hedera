from django.core.management.base import BaseCommand

from lattices.models import FormNode, LatticeNode, LemmaNode
from lemmatized_text.models import (
    LemmatizationLog,
    LemmatizedText,
    LemmatizedTextBookmark
)
from vocab_list.models import (
    PersonalVocabularyList,
    PersonalVocabularyListEntry,
    PersonalVocabularyStats,
    VocabularyList,
    VocabularyListEntry
)


MODELS = [
    LemmatizedText,
    LatticeNode,
    VocabularyList,
    PersonalVocabularyList,
    FormNode,
    LemmaNode,
    LemmatizationLog,
    LemmatizedTextBookmark,
    VocabularyListEntry,
    PersonalVocabularyListEntry,
    PersonalVocabularyStats
]


def delete_all_objects(model):
    num_deleted, _ = model.objects.all().delete()
    return num_deleted


class Command(BaseCommand):
    help = "Deletes all data from lattices, lemmatized_text, and vocab_list"

    def add_arguments(self, parser):
        parser.add_argument("--no_input", action="store_true", help="Automatic 'yes' to all prompts")

    def handle(self, *args, **options):
        """Deletes all data from lattices, lemmatized_text, and vocab_list"""
        self.deletion_loop(MODELS, options["no_input"])
        return 0

    def deletion_loop(self, model_list, no_input):
        for model in model_list:
            if model.objects.count() == 0:
                self.stdout.write(f"There are no {model} objects to delete")
                continue
            if not no_input:
                confirmation = input(f"Delete all objects from {model}? y/n ")
                if confirmation == "y":
                    self.exectute_deletion(model)
                else:
                    self.stdout.write(f"Skipping {model} data deletion")
            else:
                self.exectute_deletion(model)

    def exectute_deletion(self, model):
        task_result = delete_all_objects(model)
        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {task_result} {model} objects"))
