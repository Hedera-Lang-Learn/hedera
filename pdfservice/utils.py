from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

import requests


def get_absolute_static_path(request):
    """
    Generate the absolute version of `settings.STATIC_URL`.
    """
    if request is None:
        host = get_current_site(None).domain
        scheme = settings.DEFAULT_HTTP_PROTOCOL
    else:
        host = request.get_host()
        scheme = request.scheme
    return f"{scheme}://{host}{settings.STATIC_URL}"


def generate_pdf(template_name, context, params, request=None, fix_static_paths=True, stream=True):
    """
    Renders a template to string and then uses the EC PDF Service to render that
    HTML to a pdf.
    If `fix_static_paths=True`, replaces static paths with the absolute path to assets
    so that the EC PDF Service can retrieve and use static assets when rendering the
    HTML.
    If `stream=True`, streams response as it arrives.
    """
    html = render_to_string(template_name, context=context, request=request)
    if fix_static_paths:
        replacement = get_absolute_static_path(request)
        html = html.replace(settings.STATIC_URL, replacement)

    r = requests.post(
        settings.PDF_SERVICE_ENDPOINT,
        json={
            "html": html
        },
        params=params,
        headers={
            "x-api-key": settings.PDF_SERVICE_TOKEN,
        },
        stream=stream
    )
    r.raise_for_status()
    return r
