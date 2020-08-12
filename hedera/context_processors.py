import socket

from django.conf import settings as django_settings

from django.contrib.sites.models import Site


def pinax_apps_filter(app):
    return app.startswith("pinax.") or app in ["account", "mailer"]


def package_names(names):
    apps = []
    for x in names:
        if x.startswith("pinax."):
            apps.append(x.replace(".", "-"))
        if x == "account":
            apps.append("django-user-accounts")
        if x == "mailer":
            apps.append("django-mailer")
    return apps


def settings(request):
    ctx = {
        "ADMIN_URL": django_settings.ADMIN_URL,
        "CONTACT_EMAIL": django_settings.CONTACT_EMAIL,
        "IS_LTI": django_settings.IS_LTI,

        "pinax_notifications_installed": "pinax.notifications" in django_settings.INSTALLED_APPS,
        "pinax_stripe_installed": "pinax.stripe" in django_settings.INSTALLED_APPS,

        "pinax_apps": package_names(filter(pinax_apps_filter, django_settings.INSTALLED_APPS))
    }

    if Site._meta.installed:
        site = Site.objects.get_current(request)
        ctx.update({
            "SITE_NAME": site.name,
            "SITE_DOMAIN": site.domain
        })

    return ctx


def vue_debug(request):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("0.0.0.0", 8098))
        debug = True
    except ConnectionRefusedError:
        print("connection failed")
        debug = False
    sock.close()
    return {
        "VUE_DEBUG": debug
    }
