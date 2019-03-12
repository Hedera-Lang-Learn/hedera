import json

from django.shortcuts import get_object_or_404, redirect, render

from lemmatization.lemmatizer import lemmatize_text

from . import models


def lemmatized_texts(request):
    return render(request, "lemmatized_text/list.html", { "lemmatized_texts": models.LemmatizedText.objects.all() })


def create(request):
    cloned_from = None
    if request.method == "POST":
        title = request.POST.get("title")
        lang = request.POST.get("lang")
        text = request.POST.get("text")
        if request.POST.get("cloned_from"):
            cloned_from = get_object_or_404(models.LemmatizedText, pk=request.POST.get("cloned_from"))
        data = lemmatize_text(text, lang)
        lt = models.LemmatizedText.objects.create(title=title, data=data, lang=lang, cloned_from=cloned_from)
        return redirect(f"/lemmatized_text/{lt.pk}")
    if request.GET.get("cloned_from"):
        cloned_from = get_object_or_404(models.LemmatizedText, pk=request.GET.get("cloned_from"))
    return render(request, "lemmatized_text/create.html", {"cloned_from": cloned_from})


def delete(request, pk):
    text = get_object_or_404(models.LemmatizedText, pk=pk)
    if request.method == "POST":
        text.delete()
        return redirect("lemmatized_texts_list")
    return render(request, "lemmatized_text/delete.html", { "text": text })


def text(request, pk):
    text = get_object_or_404(models.LemmatizedText, pk=pk)
    return render(request, "lemmatized_text/text.html", { "text": text })


def learner_text(request, pk):
    text = get_object_or_404(models.LemmatizedText, pk=pk)
    return render(request, "lemmatized_text/learner_text.html", { "text": text })
