from django.http import Http404
from django.shortcuts import render

from .text_provider import get_text


def read(request, text_id):
    text = get_text(text_id)
    if text is None:
        raise Http404("Text does not exist")
    return render(request, "read.html", {
        "text": text
    })
