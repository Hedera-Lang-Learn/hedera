import logging

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import models


def lemmatized_texts(request):
    return render(request, "lemmatized_text/list.html")


def create(request):
    cloned_from = None
    select_lang = ""
    # create the  selected language here, which is the lanaguage of the last submitted text
    try:
        select_lang = models.LemmatizedText.objects.filter(Q(created_by=request.user)).order_by("-pk")[0].lang
    except Exception as e:
        logging.exception(e)

    # the POST is after form is submitted
    if request.method == "POST":
        title = request.POST.get("title")
        lang = request.POST.get("lang")
        text = request.POST.get("text")
        if request.POST.get("cloned_from"):
            cloned_from = get_object_or_404(models.LemmatizedText, pk=request.POST.get("cloned_from"))
        lt = models.LemmatizedText.objects.create(
            title=title,
            lang=lang,
            data={},
            original_text=text,
            cloned_from=cloned_from,
            created_by=request.user
        )
        lt.lemmatize()
        return redirect("lemmatized_texts_list")

    # the GET is for initial page or getting the cloned from object
    if request.GET.get("cloned_from"):
        cloned_from = get_object_or_404(models.LemmatizedText, pk=request.GET.get("cloned_from"))

    # if the text is being cloned then make sure that language is the selected one
    if cloned_from:
        select_lang = cloned_from.lang

    return render(request, "lemmatized_text/create.html", {"cloned_from": cloned_from, "select_lang": select_lang})


@require_POST
def retry_lemmatization(request, pk):
    text = get_object_or_404(models.LemmatizedText, pk=pk, created_by=request.user)
    text.retry_lemmatization()
    return redirect("lemmatized_texts_list")


@require_POST
def cancel_lemmatization(request, pk):
    text = get_object_or_404(models.LemmatizedText, pk=pk, created_by=request.user)
    text.cancel_lemmatization()
    return redirect("lemmatized_texts_list")


def delete(request, pk):
    text = get_object_or_404(models.LemmatizedText, pk=pk, created_by=request.user)
    if request.method == "POST":
        text.delete()
        return redirect("lemmatized_texts_list")
    return render(request, "lemmatized_text/delete.html", {"text": text})


def text(request, pk):
    qs = models.LemmatizedText.objects.filter(
        Q(public=True) |
        Q(created_by=request.user) |
        Q(classes__teachers=request.user)
    )
    text = get_object_or_404(qs, pk=pk)
    return render(request, "lemmatized_text/text.html", {"text": text})


def learner_text(request, pk):
    qs = models.LemmatizedText.objects.filter(
        Q(public=True) |
        Q(created_by=request.user) |
        Q(classes__students=request.user) |
        Q(classes__teachers=request.user)
    ).distinct()
    text = get_object_or_404(qs, pk=pk)
    return render(request, "lemmatized_text/learner_text.html", {"text": text})


def lemma_status(request, pk):
    lemma = models.LemmatizedText.objects.get(pk=pk)
    status = lemma.completed
    length = lemma.token_count()
    return JsonResponse({"status": status, "len": length})
