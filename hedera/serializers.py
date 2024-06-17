from rest_framework import serializers

from vocab_list.models import Folder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'description', 'created_at', 'vocab_lists']
