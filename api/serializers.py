# api/serializers.py

from rest_framework import serializers
from documents.models import Document
from django.contrib.auth import get_user_model # Лучше использовать get_user_model

User = get_user_model() # Получаем активную модель пользователя

class DocumentSerializer(serializers.ModelSerializer):
    # Отображаем username автора, только для чтения
    author_username = serializers.CharField(source='author.username', read_only=True)
    # Поле author для связи, используем PrimaryKeyRelatedField для записи ID
    # Оно будет read_only=True, так как автор назначается во view
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)


    class Meta:
        model = Document
        # Убери 'author' из fields, если не хочешь чтобы ID автора отдавался/принимался напрямую
        # Оставим для примера, но сделаем read_only ниже или во view
        fields = ['id', 'title', 'content', 'author', 'author_username', 'created_at', 'updated_at']
        # Указываем, что автор не должен приниматься напрямую из запроса,
        # т.к. мы его устанавливаем во view при создании/обновлении
        read_only_fields = ['author', 'author_username', 'created_at', 'updated_at']

    # Опционально: если хочешь разрешить создание документа без автора через API
    # def validate_author(self, value):
    #     # По умолчанию автор будет установлен во view из request.user
    #     # Этот валидатор нужен, если бы мы разрешали передавать author в запросе
    #     return value