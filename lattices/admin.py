from django.contrib import admin

from . import models


admin.site.register(models.LatticeNode)
admin.site.register(models.FormNode)
admin.site.register(models.LemmaNode)
