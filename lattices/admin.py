from django.contrib import admin

from . import models


class LatticeNodeAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "gloss", "canonical")


admin.site.register(models.LatticeNode, LatticeNodeAdmin)
admin.site.register(models.LemmaNode)
