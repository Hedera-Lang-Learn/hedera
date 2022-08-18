from django.contrib import admin

from . import models


class LemmaAdmin(admin.ModelAdmin):
    list_display = ("lang", "lemma", "alt_lemma", "label", "rank")
    search_fields = ["lemma__iexact"]


class FormToLemmaAdmin(admin.ModelAdmin):
    list_display = ("lang", "form", "lemma")
    search_fields = ["form__iexact"]


class GlossAdmin(admin.ModelAdmin):
    list_display = ("lemma", "gloss")
    search_fields = ["lemma__iexact"]


admin.site.register(models.Lemma, LemmaAdmin)
admin.site.register(models.FormToLemma, FormToLemmaAdmin)
admin.site.register(models.Gloss, GlossAdmin)
