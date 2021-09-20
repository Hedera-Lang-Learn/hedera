from django.core.management.base import BaseCommand

from lattices import LatticeNode, FormNode, LemmaNode
from lemmatized_text import LemmatizedText, LemmatizationLog, LemmatizedTextBookmark
from vocab_list import VocabularyList, VocabularyListEntry, PersonalVocabularyList, PersonalVocabularyListEntry, PersonalVocabularyStats

PRIMARY_MODELS = [
    LemmatizedText,
    LatticeNode,
    VocabularyList,
    PersonalVocabularyList
]

RELATED_MODELS = [
    FormNode,
    LemmaNode,
    LemmatizationLog,
    LemmatizedTextBookmark,
    VocabularyListEntry,
    PersonalVocabularyListEntry,
    PersonalVocabularyStats
]

def delete_all_objects(model):
    try:
        num_deleted, _ = model.objects.all().delete()
        return num_deleted
    except:
        return False


class Command(BaseCommand):
    help = "Deletes all data from lattices, lemmatized_text, and vocab_list"

    def add_arguments(self, parser):
        parser.add_argument("--no_input", action="store_true", help="Automatic 'yes' to all prompts")

    def handle(self, *args, **options):
        """Deletes all data from lattices, lemmatized_text, and vocab_list"""

        for model in PRIMARY_MODELS:
            if not options["no_input"]:
                confirmation = input(f"Delete all objects from {model}? y/n")
                if confirmation == "y":
                    self.exectute_deletion(model)
                else:
                    self.stdout.write(f"Skipping {model} data deletion")
            else:
                self.exectute_deletion(model)

        for model in RELATED_MODELS:
            if not options["no_input"]:
                if model.objects.count() > 0:
                    confirmation = input(f"Delete all objects from {model}? y/n")
                    if confirmation == "y":
                        self.exectute_deletion(model)
                    else:
                        self.stdout.write(f"Skipping {model} data deletion")
                else:
                    self.stdout.write(f"There are no {model} objects to delete")
            else:
                self.exectute_deletion(model)

        return 0

    def exectute_deletion(self, model):
        task_result = delete_all_objects(model)
        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {task_result} {model} objects"))
