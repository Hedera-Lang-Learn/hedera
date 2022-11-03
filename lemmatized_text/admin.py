from django.contrib import admin

from .models import LemmatizedText


class LemmatizedTextAdmin(admin.ModelAdmin):
    list_display = ("lang", "title", "public", "created_by", "created_at")
    search_fields = ["title__iexact"]


admin.site.register(LemmatizedText, LemmatizedTextAdmin)
