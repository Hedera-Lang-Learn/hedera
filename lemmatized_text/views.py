import json

from django.shortcuts import get_object_or_404, render

from . import models
from lattices.models import LatticeNode


def read(request, text_id):
    text = get_object_or_404(models.LemmatizedText, pk=text_id)

    data = []

    for item in json.loads(text.data):
        node = LatticeNode.objects.get(pk=item["node"])
        data.append({
            "token": item["token"],
            "node": node,
            "resolved": item["resolved"],
        })


    return render(request, "lemmatized_text/read.html", {
        "data": data,
    })
