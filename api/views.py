from rest_framework import viewsets
from documents.models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly # Для стандартного


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()