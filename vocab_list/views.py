from django.views.generic import DetailView, ListView

from .models import VocabularyList, PersonalVocabularyList


class VocabularyListListView(ListView):

    template_name = "vocab_list/list.html"
    model = VocabularyList


class VocabularyListDetailView(DetailView):

    template_name = "vocab_list/detail.html"
    model = VocabularyList


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
