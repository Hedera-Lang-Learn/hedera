
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from django.contrib import admin

from . import api, views


urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    path("admin/", admin.site.urls),
    re_path(r"^account/", include("account.urls")),

    path("read/<int:text_id>/", views.read, name="read"),

    path("lemmatized_text/", include("lemmatized_text.urls")),
    path("lattices/", include("lattices.urls")),

    path("api/v1/lemmatized_texts/<int:pk>/detail/", api.LemmatizedTextDetailAPI.as_view()),
    path("api/v1/lemmatized_texts/<int:pk>/", api.LemmatizationAPI.as_view()),
    path("api/v1/vocab_lists/", api.VocabularyListAPI.as_view()),
]
