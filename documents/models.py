from django.db import models
from django.conf import settings
from django.urls import reverse

class Document(models.Model):
    objects = None
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_create_document", "Can create document"),
            ("can_edit_document", "Can edit document"),
            ("can_delete_document", "Can delete document"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document_detail', kwargs={'pk': self.pk})