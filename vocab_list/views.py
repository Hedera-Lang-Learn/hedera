from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import PersonalVocabularyListForm, VocabularyListForm
from .models import PersonalVocabularyList, VocabularyList


class VocabularyListListView(ListView):

    template_name = "vocab_list/list.html"
    model = VocabularyList


class VocabularyListDetailView(DetailView):

    template_name = "vocab_list/detail.html"
    model = VocabularyList


class VocabularyListDeleteView(DeleteView):

    template_name = "vocab_list/delete.html"
    model = VocabularyList

    def get_success_url(self):
        return reverse("vocab_list_list")


class VocabularyListCreateView(CreateView):

    template_name = "vocab_list/create.html"
    model = VocabularyList
    form_class = VocabularyListForm

    def form_valid(self, form):
        vl = form.save()
        entries = vl.load_tab_delimited(form.cleaned_data["data"])
        for entry in entries:
            entry.link_job()
        return redirect(reverse("vocab_list_detail", args=[vl.pk]))


class PersonalVocabListDetailView(DetailView):

    template_name = "vocab_list/personal.html"
    model = PersonalVocabularyList
    slug_field = "lang"
    slug_url_kwarg = "lang"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vocab_list = self.get_object()
        context.update({
            "lists": vocab_list.user.personalvocabularylist_set.all().order_by("lang")
        })
        return context


class PersonalVocabularyListEntriesCreateView(CreateView):

    template_name = "vocab_list/personal_create.html"
    model = PersonalVocabularyList
    form_class = PersonalVocabularyListForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "lists": self.request.user.personalvocabularylist_set.all().order_by("lang")
        })
        return context

    def form_valid(self, form):
        vl, _ = PersonalVocabularyList.objects.get_or_create(user=self.request.user, lang=form.cleaned_data["lang"])
        entries = vl.load_tab_delimited(form.cleaned_data["data"], familiarity=form.cleaned_data["rating"])
        # @@@ kick off background tasks for linking the entries
        return redirect(reverse("vocab_list_personal_detail", args=[vl.lang]))
