import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from lattices.utils import get_or_create_nodes_for_form_and_lemmas
from lemmatized_text.models import LemmatizedText
from vocab_list.models import VocabularyList

class APIView(View):

    def get_data(self):
        return {}

    def render_to_response(self):
        return JsonResponse({"data": self.get_data()})

    def get(self, request, *args, **kwargs):
        return self.render_to_response()


class LemmatizationAPI(APIView):

    def get_data(self):
        text = get_object_or_404(LemmatizedText, pk=self.kwargs.get("pk"))
        return json.loads(text.data)

    def post(self, request, *args, **kwargs):
        text = get_object_or_404(LemmatizedText, pk=self.kwargs.get("pk"))
        data = json.loads(request.body)
        token_index = data["tokenIndex"]
        node_id = data["nodeId"]
        resolved = data["resolved"]

        text_data = json.loads(text.data)

        if node_id is None:
            form = text_data[token_index]["token"]
            node_id = get_or_create_nodes_for_form_and_lemmas(form, [data["lemma"]], context="user").pk

        text_data[token_index]["node"] = node_id
        text_data[token_index]["resolved"] = resolved
        text.data = json.dumps(text_data)
        text.save()

        text.refresh_from_db()
        return JsonResponse({"data": json.loads(text.data)})


class VocabularyListAPI(APIView):

    def get_data(self):
        return [v.data() for v in VocabularyList.objects.all()]
