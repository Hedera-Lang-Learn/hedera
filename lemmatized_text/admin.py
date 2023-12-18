from django.contrib import admin

from .models import LemmatizedText, LemmatizedTextBookmark


class LemmatizedTextAdmin(admin.ModelAdmin):
    list_display = ("lang", "title", "public", "created_by", "created_at")
    search_fields = ["title__iexact"]


admin.site.register(LemmatizedText, LemmatizedTextAdmin)

class LemmatizedTextAdminBookmark(admin.ModelAdmin):
    list_display = ("text", "user_id", "created_at", "read_status")

admin.site.register(LemmatizedTextBookmark, LemmatizedTextAdminBookmark)
