
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from django.contrib import admin

from . import views


urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    path("admin/", admin.site.urls),
    re_path(r"^account/", include("account.urls")),

    path("read/<int:text_id>/", views.read, name="read"),
]
