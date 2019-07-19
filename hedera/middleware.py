import re

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.http import urlquote


class AuthenticatedMiddleware(object):
    def __init__(self, get_response, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
        self.get_response = get_response
        if login_url is None:  # pragma: no cover
            login_url = settings.LOGIN_URL
        self.login_url = reverse_lazy(login_url)
        self.redirect_field_name = redirect_field_name
        self.exemptions = [
            r"^%s" % settings.MEDIA_URL,
            r"^%s" % settings.STATIC_URL,
            r"^%s$" % self.login_url,
        ] + getattr(settings, "AUTHENTICATED_EXEMPT_URLS", [])

    def __call__(self, request):
        for exemption in self.exemptions:
            if re.match(exemption, request.path):
                response = self.get_response(request)
                return response
        if not request.user.is_authenticated:
            path = urlquote(request.get_full_path())
            tup = (self.login_url, self.redirect_field_name, path)
            if request.is_ajax() or request.META.get("HTTP_X_VUE_FRONTEND") == "Made by Eldarion":
                tup = (tup[0], tup[1], request.META.get("HTTP_REFERER").replace(request.META.get("HTTP_ORIGIN"), ""))
                return JsonResponse({
                    "error": "You must login to see this",
                    "location": "%s?%s=%s" % tup
                }, status=403)
            return HttpResponseRedirect("%s?%s=%s" % tup)
        else:
            response = self.get_response(request)
            return response
