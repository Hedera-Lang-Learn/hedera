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
        print(LemmatizedText.objects.all())
        text = get_object_or_404(LemmatizedText, pk=self.kwargs.get("pk"))
        return json.loads(text.data)
