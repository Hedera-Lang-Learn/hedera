
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from django.contrib import admin

from . import views
from . import api


urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    path("admin/", admin.site.urls),
    re_path(r"^account/", include("account.urls")),

    path("read/<int:text_id>/", views.read, name="read"),

    # path("lemmatized_text/", include("lemmatized_text.urls")),
    path("lattices/", include("lattices.urls")),

    path("api/v1/texts/<int:pk>/", api.LemmatizationAPI.as_view()),

    path("<path:path>", views.app),
]
