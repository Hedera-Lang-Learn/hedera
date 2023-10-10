from django.contrib import admin

from .models import LemmatizedText
from .models import LemmatizedTextBookmark

class LemmatizedTextAdmin(admin.ModelAdmin):
    list_display = ("lang", "title", "public", "created_by", "created_at")
    search_fields = ["title__iexact"]


admin.site.register(LemmatizedText, LemmatizedTextAdmin)

class LemmatizedTextAdminBookmark(admin.ModelAdmin):
    # list_display = ("created_at", "user_id", "read_status")
    # search_fields = ["title__iexact"]
    pass

admin.site.register(LemmatizedTextBookmark, LemmatizedTextAdminBookmark)
