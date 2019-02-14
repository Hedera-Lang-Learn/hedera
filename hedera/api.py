import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from lattices.models import LatticeNode
from lemmatized_text.models import LemmatizedText


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
        text_data[token_index]["node"] = node_id
        text_data[token_index]["resolved"] = resolved
        text.data = json.dumps(text_data)
        text.save()

        text.refresh_from_db()
        return JsonResponse({"data": json.loads(text.data)})
