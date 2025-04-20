from rest_framework import serializers
from documents.models import Document
from django.contrib.auth import get_user_model

User = get_user_model() # Получаем активн модель юсера

class DocumentSerializer(serializers.ModelSerializer):

    author_username = serializers.CharField(source='author.username', read_only=True)

    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)


    class Meta:
        model = Document

        fields = ['id', 'title', 'content', 'author', 'author_username', 'created_at', 'updated_at']

        read_only_fields = ['author', 'author_username', 'created_at', 'updated_at']

