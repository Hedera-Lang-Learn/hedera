import uuid

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from account.views import SettingsView as AccountSettingsView
from account.views import SignupView as AccountSignupView

from .forms import SettingsForm, SignupForm
from .text_provider import get_text


def read(request, text_id):
    text = get_text(text_id)
    if text is None:
        raise Http404("Text does not exist")
    return render(request, "read.html", {
        "text": text
    })


class SettingsView(AccountSettingsView):

    form_class = SettingsForm

    def update_settings(self, form):
        if settings.IS_LTI:
            form.cleaned_data["email"] = self.request.user.email
        super().update_settings(form)
        profile = self.request.user.profile
        profile.display_name = form.cleaned_data["display_name"]
        profile.show_node_ids = form.cleaned_data["show_node_ids"]
        profile.save()

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            "display_name": self.request.user.profile.display_name,
            "show_node_ids": self.request.user.profile.show_node_ids,
        })
        return initial


class SignupView(AccountSignupView):

    form_class = SignupForm
    identifier_field = "email"

    def generate_username(self, form):
        return str(uuid.uuid4())

    def after_signup(self, form):
        profile = self.created_user.profile
        profile.display_name = form.cleaned_data["display_name"]
        profile.save()


# https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-loginrequired-mixin
class DashboardView(LoginRequiredMixin, TemplateView):

    login_url = "/account/login/"
    template_name = "dashboard.html"
