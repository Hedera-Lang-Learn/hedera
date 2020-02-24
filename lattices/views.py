from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import LatticeNode


def node_json(request, node_id):
    node = get_object_or_404(LatticeNode, pk=node_id)

    return JsonResponse(node.to_dict())
