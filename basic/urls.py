
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from django.contrib import admin


urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    path("admin/", admin.site.urls),
    re_path(r"^account/", include("account.urls")),
]
