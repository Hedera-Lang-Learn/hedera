
from django.urls import path, re_path, include
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    re_path(r"^account/", include("account.urls")),
]
