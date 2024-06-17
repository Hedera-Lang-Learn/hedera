from vocab_list.models import Folder
from django.rest_framework import serializers


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'description', 'created_at', 'vocab_lists']
