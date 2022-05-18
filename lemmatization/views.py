from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Lemma


def lemma_json(request, lemma_id):
    lemma = get_object_or_404(Lemma, pk=lemma_id)
    return JsonResponse(lemma.to_dict())
