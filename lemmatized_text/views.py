from django.shortcuts import get_object_or_404, redirect, render

from . import models


def lemmatized_texts(request):
    return render(request, "lemmatized_text/list.html", { "lemmatized_texts": models.LemmatizedText.objects.all().order_by("pk") })


def create(request):
    cloned_from = None
    if request.method == "POST":
        title = request.POST.get("title")
        lang = request.POST.get("lang")
        text = request.POST.get("text")
        if request.POST.get("cloned_from"):
            cloned_from = get_object_or_404(models.LemmatizedText, pk=request.POST.get("cloned_from"))
        lt = models.LemmatizedText.objects.create(title=title, lang=lang, data={}, cloned_from=cloned_from)
        lt.lemmatize(text, lang)
        return redirect("lemmatized_texts_list")
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
