import json

from django.shortcuts import get_object_or_404, redirect, render

from . import models
from lemmatization.lemmatizer import lemmatize_text


def lemmatized_texts(request):
    return render(request, "lemmatized_text/list.html", { "lemmatized_texts": models.LemmatizedText.objects.all() })


def create(request):
    if request.method == "POST":
        lang = request.POST.get("lang")
        text = request.POST.get("text")
        data = json.dumps(lemmatize_text(text, lang))
        lt = models.LemmatizedText.objects.create(data=data)
        return redirect(f"/lemmatized_text/{lt.pk}")
    return render(request, "lemmatized_text/create.html", {})


def text(request, pk):
    text = get_object_or_404(models.LemmatizedText, pk=pk)
    return render(request, "lemmatized_text/text.html", { "text": text })
