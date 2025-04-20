# documents/views.py

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Document
from .forms import DocumentForm # Убедись, что файл documents/forms.py тоже есть и содержит DocumentForm

class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10 # Количество документов на странице

    def get_queryset(self):
        # Получаем базовый queryset
        queryset = super().get_queryset().select_related('author') # Оптимизация запроса автора

        # Получаем параметры поиска и сортировки из GET-запроса
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        # Фильтрация по поисковому запросу (title или content)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        # Сортировка
        if sort == 'title':
            queryset = queryset.order_by('title')
        elif sort == 'date':
            queryset = queryset.order_by('-created_at') # По умолчанию (самые новые сначала)
        else:
             queryset = queryset.order_by('-created_at') # По умолчанию

        return queryset

    def get_context_data(self, **kwargs):
        # Добавляем текущие параметры поиска и сортировки в контекст
        # для использования в шаблоне (например, чтобы сохранить их в пагинации)
        context = super().get_context_data(**kwargs)
        context['current_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'date')
        return context


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'
    # Оптимизация запроса автора
    queryset = Document.objects.select_related('author').all()


class DocumentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    permission_required = 'documents.can_create_document' # Право из модели Document
    # success_url = reverse_lazy('document_list') # Можно и так, но get_absolute_url предпочтительнее

    # Автоматически устанавливаем автора при сохранении формы
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    permission_required = 'documents.can_edit_document' # Право из модели Document
    # success_url = reverse_lazy('document_list') # get_absolute_url сработает
    queryset = Document.objects.select_related('author').all() # Оптимизация

    # Опционально: Дополнительная проверка, если редактировать может только автор
    # def get_queryset(self):
    #    queryset = super().get_queryset()
    #    # Показываем только документы текущего пользователя для редактирования (если не суперюзер)
    #    if not self.request.user.is_superuser:
    #        return queryset.filter(author=self.request.user)
    #    return queryset


class DocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Document
    template_name = 'documents/document_confirm_delete.html'
    success_url = reverse_lazy('document_list') # После удаления переходим на список
    permission_required = 'documents.can_delete_document' # Право из модели Document
    queryset = Document.objects.select_related('author').all() # Оптимизация

    # Опционально: Аналогичная проверка как в UpdateView
    # def get_queryset(self):
    #    # ...