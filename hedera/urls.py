from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from django.contrib import admin

from account.forms import LoginEmailForm
from account.views import LoginView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from lti.views import LtiInitializerView

from . import api, views


urlpatterns = [
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    path("admin/", admin.site.urls),
    path("django-rq/", include("django_rq.urls")),
    path("account/login/", LoginView.as_view(form_class=LoginEmailForm), name="account_login"),
    path("account/signup/", views.SignupView.as_view(), name="account_signup"),
    path("account/settings/", views.SettingsView.as_view(), name="account_settings"),
    path("account/", include("account.urls")),

    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),

    path("lemmatized_text/", include("lemmatized_text.urls")),
    path("lattices/", include("lattices.urls")),
    path("vocab/", include("vocab_list.urls")),

    path("classes/", include("groups.urls")),

    path("api/v1/me/", api.MeAPI.as_view()),
    path("api/v1/bookmarks/", api.BookmarksListAPI.as_view()),
    path("api/v1/bookmarks/<int:pk>/", api.BookmarksDetailAPI.as_view()),
    path("api/v1/lemmatization/lemma/<int:lemma_id>/", api.LemmatizationLemmaAPI.as_view()),
    path("api/v1/lemmatization/forms/<str:lang>/<str:form>/", api.LemmatizationFormLookupAPI.as_view()),
    path("api/v1/lemmatization/partial_match_forms/<str:lang>/<str:form>/", api.PartialMatchFormLookupAPI.as_view()),
    path("api/v1/lemmatized_texts/", api.LemmatizedTextListAPI.as_view()),
    path("api/v1/lemmatized_texts/<int:pk>/detail/", api.LemmatizedTextDetailAPI.as_view()),
    path("api/v1/lemmatized_texts/<int:pk>/status/", api.LemmatizedTextStatusAPI.as_view()),
    path("api/v1/lemmatized_texts/<int:pk>/<str:action>/", api.LemmatizedTextStatusAPI.as_view()),
    path("api/v1/lemmatized_texts/<int:pk>/", api.LemmatizationAPI.as_view()),
    path("api/v1/lemmatized_texts/<int:pk>/tokens/<int:token_index>/history/", api.TokenHistoryAPI.as_view()),
    path("api/v1/vocab_lists/", api.VocabularyListAPI.as_view()),
    path("api/v1/vocab_lists/<int:pk>/entries/", api.VocabularyListEntriesAPI.as_view()),
    path("api/v1/vocab_entries/<int:pk>/<str:action>/", api.VocabularyListEntryAPI.as_view()),
    path("api/v1/personal_vocab_list/", api.PersonalVocabularyListAPI.as_view()),
    path("api/v1/personal_vocab_list/<int:pk>/", api.PersonalVocabularyListAPI.as_view()),
    path("api/v1/personal_vocab_list/quick_add/", api.PersonalVocabularyQuickAddAPI.as_view()),
    path("api/v1/supported_languages/", api.SupportedLanguagesAPI.as_view()),

    path("lti/", include("lti_provider.urls")),
    path("lti/lti_initializer/", LtiInitializerView.as_view(), name="lti_initializer"),

    path("cms/", include(wagtailadmin_urls)),
    re_path(r"", include(wagtail_urls)),

] + static(
    settings.STATIC_URL, document_root=settings.STATIC_URL
) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
