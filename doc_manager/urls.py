# Путь: doc_manager/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),

    # Вот здесь добавляем namespace='api'
    path('api/', include(('api.urls', 'api'), namespace='api')),

    path('', include('pages.urls')),
    path('docs/', include('documents.urls')),
]