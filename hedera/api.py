import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from lattices.models import LatticeNode
# from lattices.utils import get_or_create_nodes_for_form_and_lemmas
from lemmatized_text.models import LemmatizedText
from vocab_list.models import (
    PersonalVocabularyList,
    PersonalVocabularyListEntry,
    PersonalVocabularyStats,
    VocabularyList,
    VocabularyListEntry
)


class JsonResponseAuthError(JsonResponse):

    status_code = 401


class AuthedView(View):

    auth_required = True

    @property
    def user(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if self.auth_required and not request.user.is_authenticated:
            return JsonResponseAuthError(data={"error": "Authentication required"})
        return super().dispatch(request, *args, **kwargs)


class APIView(AuthedView):

    def get_data(self):
        return {}

    def render_to_response(self):
        return JsonResponse({"data": self.get_data()})

    def get(self, request, *args, **kwargs):
        return self.render_to_response()


class LemmatizedTextListAPI(APIView):

    def get_data(self):
        qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user)).order_by("created_at")
        return [
            dict(text=text.api_data(), stats=text.stats_for_user(self.request.user))
            for text in qs
        ]


class LemmatizedTextStatusAPI(APIView):

    @property
    def text(self):
        if not hasattr(self, "_text"):
            qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
            self._text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        return self._text

    def get_data(self):
        return dict(
            completed=self.text.completed,
            tokenCount=self.text.token_count() if self.text.completed == 100 else None,
            lemmatizationStatus=self.text.lemmatization_status(),
        )

    def post(self, request, *args, **kwargs):
        if self.kwargs.get("action") == "retry" and self.text.can_retry():
            self.text.retry_lemmatization()
        elif self.kwargs.get("action") == "cancel" and self.text.can_cancel():
            self.text.cancel_lemmatization()
        self.text.refresh_from_db()
        return JsonResponse(data=dict(data=self.get_data()))


class LemmatizedTextDetailAPI(APIView):

    def get_data(self):
        qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
        text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        return text.api_data()


class LemmatizationAPI(APIView):

    def decorate_token_data(self, text):
        data = text.data
        nodes = LatticeNode.objects.filter(pk__in=[token["node"] for token in data])
        if self.request.GET.get("vocablist", None) is not None:
            vl = get_object_or_404(VocabularyList, pk=self.request.GET.get("vocablist"))
            for token in data:
                node = nodes.filter(pk=token["node"]).first()  # does doing this avoid a second trip to the database?
                if node is not None:
                    token["inVocabList"] = token["resolved"] and vl.entries.filter(node__in=node.related_nodes()).exists()
                else:
                    token["inVocabList"] = False

        if self.request.GET.get("personalvocablist", None) is not None:
            vl = get_object_or_404(PersonalVocabularyList, pk=self.request.GET.get("personalvocablist"))
            for token in data:
                token["inVocabList"] = token["resolved"] and vl.entries.filter(node__pk=token["node"]).exists()
                token["familiarity"] = token["resolved"] and vl.node_familiarity(token["node"])

        for token in data:
            node = nodes.filter(pk=token["node"]).first()
            if node is not None:
                token.update(node.gloss_data())

        return data

    def get_data(self):
        qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
        text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        data = self.decorate_token_data(text)
        return data

    def post(self, request, *args, **kwargs):
        qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
        text = get_object_or_404(qs, pk=self.kwargs.get("pk"))
        data = json.loads(request.body)
        token_index = data["tokenIndex"]
        node_id = data["nodeId"]
        resolved = data["resolved"]

        text_data = text.data

        if node_id is None:
            form = text_data[token_index]["token"]
            # node_id = get_or_create_nodes_for_form_and_lemmas(form, [data["lemma"]], context="user").pk

        text_data[token_index]["node"] = node_id
        text_data[token_index]["resolved"] = resolved
        text.data = text_data
        text.save()

        text.refresh_from_db()
        data = self.decorate_token_data(text)
        return JsonResponse({"data": data})


class VocabularyListAPI(APIView):

    def get_data(self):
        return [v.data() for v in VocabularyList.objects.filter(lang=self.request.GET.get("lang"))]


class VocabularyListEntriesAPI(APIView):

    def get_data(self):
        vocab_list = get_object_or_404(VocabularyList, pk=self.kwargs.get("pk"))
        return [v.data() for v in vocab_list.entries.all().order_by("headword")]


class VocabularyListEntryAPI(APIView):

    def post(self, request, *args, **kwargs):
        entry = get_object_or_404(VocabularyListEntry, pk=self.kwargs.get("pk"))

        data = json.loads(request.body)
        node = get_object_or_404(LatticeNode, pk=data["node"])
        entry.node = node
        entry.save()

        return JsonResponse(entry.data())


class PersonalVocabularyListAPI(APIView):

    @property
    def text(self):
        if self.request.GET.get("text") is None:
            return
        if getattr(self, "_text", None) is None:
            qs = LemmatizedText.objects.filter(Q(public=True) | Q(created_by=self.request.user))
            self._text = get_object_or_404(qs, pk=self.request.GET.get("text"))
        return self._text

    def get_object(self):
        if self.text:
            lang = self.text.lang
        else:
            lang = self.request.GET.get("lang")
        vl, _ = PersonalVocabularyList.objects.get_or_create(
            user=self.request.user,
            lang=lang,
        )
        return vl

    def get_data(self):
        vl = self.get_object()
        return dict(
            personalVocabList=vl.data(),
            unknownGlosses=None
        )

    def post(self, request, *args, **kwargs):
        vl = self.get_object()

        data = json.loads(request.body)
        familiarity = int(data["familiarity"])

        pk = kwargs.get("pk", None)
        if pk is not None:
            entry = get_object_or_404(PersonalVocabularyListEntry, pk=pk)
            entry.familiarity = familiarity
            entry.save()
        else:
            node = get_object_or_404(LatticeNode, pk=data["nodeId"])
            headword = data["headword"]
            gloss = data["gloss"]
            vl.entries.create(
                headword=headword,
                gloss=gloss,
                familiarity=familiarity,
                node=node,
            )

        if self.text:
            stats, _ = PersonalVocabularyStats.objects.get_or_create(text=self.text, vocab_list=vl)
            stats.update()

        vl.refresh_from_db()

        return JsonResponse({"data": vl.data()})
