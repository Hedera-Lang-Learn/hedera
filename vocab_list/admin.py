from django.contrib import admin

from . import models


@admin.register(models.VocabularyList)
class VocabularyListAdmin(admin.ModelAdmin):
    list_display = ["title", "owner"]


@admin.register(models.VocabularyListEntry)
class VocabularyListEntryAdmin(admin.ModelAdmin):
    list_display = ["id", "headword", "gloss", "vocabulary_list"]


@admin.register(models.PersonalVocabularyList)
class PersonalVocabularyListAdmin(admin.ModelAdmin):
    list_display = ["user", "lang"]


@admin.register(models.PersonalVocabularyListEntry)
class PersonalVocabularyListEntryAdmin(admin.ModelAdmin):
    list_display = ["id", "vocabulary_list", "headword", "gloss", "familiarity"]
