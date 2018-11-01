from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


def get_backends():
    backends = []
    for backend_path in settings.TEXT_PROVIDER_BACKENDS:
        backend = import_string(backend_path)()
        backends.append(backend)
    if not backends:
        raise ImproperlyConfigured(
            "No text provider backends have been defined. Does "
            "TEXT_PROVIDER_BACKENDS contain anything?"
        )
    return backends


def get_text(identifier):
    for backend in get_backends():
        text = backend.get_text(identifier)
        if text:
            return text
