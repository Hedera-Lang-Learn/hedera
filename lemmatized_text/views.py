import logging

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from lattices.models import LatticeNode
from pdfservice.mixins import PDFResponseMixin

from . import models
from .forms import LemmatizedTextEditForm


def lemmatized_texts(request):
    return render(request, "lemmatized_text/list.html")


def create(request):
    select_lang = ""
    # create the  selected language here, which is the lanaguage of the last submitted text
    try:
        select_lang = models.LemmatizedText.objects.filter(created_by=request.user).order_by("-pk")[0].lang
    except Exception as e:
        logging.exception(e)

    # the POST is after form is submitted
    if request.method == "POST":
        title = request.POST.get("title")
        lang = request.POST.get("lang")
        text = request.POST.get("text")
        lt = models.LemmatizedText.objects.create(
            title=title,
            lang=lang,
            data={},
            original_text=text,
            created_by=request.user
        )
        lt.lemmatize()
        return redirect("lemmatized_texts_list")

    # the GET is for initial page or getting the cloned from object
    if request.GET.get("cloned_from"):
        lemmatized_text = get_object_or_404(models.LemmatizedText, pk=request.GET.get("cloned_from"))
        lemmatized_text.clone(cloned_by=request.user)
        return redirect("lemmatized_texts_list")

    return render(request, "lemmatized_text/create.html", {"select_lang": select_lang, "supported_lang": settings.SUPPORTED_LANGUAGES})


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


def edit(request, pk):
    lemmatized_text = get_object_or_404(models.LemmatizedText, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = LemmatizedTextEditForm(request.POST)
        if form.is_valid():
            # pass to a "lemmatized text method" to handle changes
            lemmatized_text.handle_edited_data(request.POST.get("title"), request.POST.get("text"))
            return redirect("lemmatized_texts_list")
    form = LemmatizedTextEditForm(
        initial={
            "text": lemmatized_text.transform_data_to_html(),
            "title": lemmatized_text.title
        }
    )
    return render(request, "lemmatized_text/edit.html", {"form": form})


def learner_text(request, pk):
    qs = models.LemmatizedText.objects.filter(
        Q(public=True) |
        Q(created_by=request.user) |
        Q(classes__students=request.user) |
        Q(classes__teachers=request.user)
    ).distinct()
    text = get_object_or_404(qs, pk=pk)
    return render(request, "lemmatized_text/learner_text.html", {"text": text, "PDF_HANDOUT_ENABLED": settings.PDF_SERVICE_ENDPOINT is not None})


def lemma_status(request, pk):
    lemma = models.LemmatizedText.objects.get(pk=pk)
    status = lemma.completed
    length = lemma.token_count()
    return JsonResponse({"status": status, "len": length})


class HandoutView(PDFResponseMixin, DetailView):
    slug_field = "secret_id"
    slug_url_kwarg = "uid"
    template_name = "lemmatized_text/handout.html"
    inline = True

    def get_queryset(self):
        return models.LemmatizedText.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.object.data
        nodes = LatticeNode.objects.filter(pk__in=[token["node"] for token in data])  # .order_by("label")
        context["words"] = nodes
        return context
