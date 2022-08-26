from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from .filters import PostFilter
from .forms import PostForm


# Список всех постов
class PostList(ListView):
    model = Post  # выводим посты
    ordering = '-time_add'  # сортировка по дате создания
    template_name = 'posts.html'  # шаблон для вывода
    context_object_name = 'posts'  # имя списка, по которому будет обращение из html-шаблона
    paginate_by = 10 # количество постов на странице

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        queryset = super().get_queryset()  # получаем обычный запрос
        self.filterset = PostFilter(self.request.GET, queryset)  # сохраняем фильтрацию в объекте класса
        return self.filterset.qs  # возвращаем отфильтрованный список постов

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset  # добавляем в контекст объект фильтрации
        # context['next_post'] = "New post will be added tomorrow!"
        return context


# Подробности по каждому посту
class PostDetail(DetailView):
    model = Post  # выводим посты
    template_name = 'post.html'  # шаблон для вывода
    context_object_name = 'post'  # имя списка, по которому будет обращение из html-шаблона


# Представление для создания поста
class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление для изменения поста (форма и шаблон как для создания поста)
class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление для удаления поста
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')  # после удаления перенаправляем на страницу со списком постов
