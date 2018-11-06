from django.contrib import admin

from . import models


@admin.register(models.VocabularyList)
class VocabularyListAdmin(admin.ModelAdmin):
    list_display = ["title", "owner"]


@admin.register(models.VocabularyListEntry)
class VocabularyListEntryAdmin(admin.ModelAdmin):
    list_display = ["id", "lemma", "gloss", "vocabulary_list"]
