# api/views.py

from rest_framework import viewsets # <--- Добавь эту строку
# from rest_framework import permissions # Это было закомментировано, но если будешь использовать кастомные, раскомментируй
from documents.models import Document
from .serializers import DocumentSerializer
# from .permissions import HasDocumentPermissionOrReadOnly # Для кастомного пермишена
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly # Для стандартного

# Дальше идет твой класс DocumentViewSet без изменений
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()