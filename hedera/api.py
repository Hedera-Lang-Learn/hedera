import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from lattices.models import LatticeNode
from lattices.utils import get_or_create_nodes_for_form_and_lemmas
from lemmatized_text.models import LemmatizedText
from vocab_list.models import PersonalVocabularyList, PersonalVocabularyListEntry, VocabularyList


class APIView(View):

    def get_data(self):
        return {}

    def render_to_response(self):
        return JsonResponse({"data": self.get_data()})

    def get(self, request, *args, **kwargs):
        return self.render_to_response()


class LemmatizedTextDetailAPI(APIView):

    def get_data(self):
        text = get_object_or_404(LemmatizedText, pk=self.kwargs.get("pk"))
        return text.api_data()


class LemmatizationAPI(APIView):

    def decorate_token_data(self, text):
        data = text.data
        if self.request.GET.get("vocablist", None) is not None:
            vl = get_object_or_404(VocabularyList, pk=self.request.GET.get("vocablist"))
            for token in data:
                token["inVocabList"] = token["resolved"] and vl.entries.filter(node__pk=token["node"]).exists()

        if self.request.GET.get("personalvocablist", None) is not None:
            vl = get_object_or_404(PersonalVocabularyList, pk=self.request.GET.get("personalvocablist"))
            for token in data:
                token["inVocabList"] = token["resolved"] and vl.entries.filter(node__pk=token["node"]).exists()
                token["familiarity"] = token["resolved"] and vl.node_familiarity(token["node"])
        return data

    def get_data(self):
        text = get_object_or_404(LemmatizedText, pk=self.kwargs.get("pk"))
        data = self.decorate_token_data(text)
        return data

    def post(self, request, *args, **kwargs):
        text = get_object_or_404(LemmatizedText, pk=self.kwargs.get("pk"))
        data = json.loads(request.body)
        token_index = data["tokenIndex"]
        node_id = data["nodeId"]
        resolved = data["resolved"]

        text_data = text.data

        if node_id is None:
            form = text_data[token_index]["token"]
            node_id = get_or_create_nodes_for_form_and_lemmas(form, [data["lemma"]], context="user").pk

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


class PersonalVocabularyListAPI(APIView):

    def get_object(self):
        vl, _ = PersonalVocabularyList.objects.get_or_create(
            user=self.request.user,
            lang=self.request.GET.get("lang"),
        )
        return vl

    def get_data(self):
        vl = self.get_object()
        return vl.data()

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
        vl.refresh_from_db()

        return JsonResponse({"data": vl.data()})

