from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post


# Список всех постов
class PostList(ListView):
    model = Post  # выводим посты
    ordering = '-time_add'  # сортировка по дате создания
    template_name = 'posts.html'  # шаблон для вывода
    context_object_name = 'posts'  # имя списка, по которому будет обращение из html-шаблона

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        # context['next_post'] = "New post will be added tomorrow!"
        return context


# Подробности по каждому посту
class PostDetail(DetailView):
    model = Post  # выводим посты
    template_name = 'post.html'  # шаблон для вывода
    context_object_name = 'post'  # имя списка, по которому будет обращение из html-шаблона
