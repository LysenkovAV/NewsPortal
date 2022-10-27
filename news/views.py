from django.contrib.sites.models import Site
from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

# Для рассылки писем
# from django.core.mail import send_mail  # для простого письма
from django.core.mail import EmailMultiAlternatives  # для письма с html
from django.template.loader import render_to_string  # функция рендеринга html в текст

from django.conf import settings
from django.contrib.sites.models import Site

import logging


logger_debug = logging.getLogger('console_debug')
logger_warning = logging.getLogger('console_warning')
logger_error = logging.getLogger('console_error')
logger_django_request = logging.getLogger('django.request')
logger_django_server = logging.getLogger('django.server')
logger_django_db_backends = logging.getLogger('django.db_backends')
logger_django_template = logging.getLogger('django.template')
logger_django_security = logging.getLogger('django.security')


# Список всех постов
class PostList(ListView):
    model = Post  # выводим посты
    ordering = '-time_add'  # сортировка по дате создания
    template_name = 'posts.html'  # шаблон для вывода
    context_object_name = 'posts'  # имя списка, по которому будет обращение из html-шаблона
    paginate_by = 10 # количество постов на странице

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        logger_error.error('TEST ERROR MESSAGE')  # тестирование логгирования
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Пока не придумал как можно подписываться/отписываться сразу на несколько категорий,
        # поэтому просто перебор всех вариантов
        context['finance'] = False
        context['sport'] = False
        context['science'] = False
        context['education'] = False
        context['IT'] = False
        context['history'] = False
        context['lifestyle'] = False
        context['travel'] = False
        # for category in self.get_object().categories.all():
        if not isinstance(self.request.user, AnonymousUser):
            if not context['finance']:
                context['finance'] = self.request.user.category_set.filter(pk=1).exists()
            if not context['sport']:
                context['sport'] = self.request.user.category_set.filter(pk=2).exists()
            if not context['science']:
                context['science'] = self.request.user.category_set.filter(pk=3).exists()
            if not context['education']:
                context['education'] = self.request.user.category_set.filter(pk=4).exists()
            if not context['IT']:
                context['IT'] = self.request.user.category_set.filter(pk=5).exists()
            if not context['history']:
                context['history'] = self.request.user.category_set.filter(pk=6).exists()
            if not context['lifestyle']:
                context['lifestyle'] = self.request.user.category_set.filter(pk=7).exists()
            if not context['travel']:
                context['travel'] = self.request.user.category_set.filter(pk=8).exists()
        return context


# Представление для создания поста с проверкой прав
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        # отправка письма с html всем пользователям, подписанным на категории поста
        category_list = Post.objects.latest("id").categories.all()  # все категории поста
        user_list = []
        email_list = []
        for cat in category_list:
            user_list = cat.subscribers.all()  # все пользователи по каждой категории
            for usr in user_list:
                email_list.append(usr.email)  # составление списка почт всех подписанных на категории пользователей
        # site = Site.objects.get_current()
        # link = f'http://{site.domain}:8000/news/{id}/'
        html_content = render_to_string(
            'mail_message_created.html',
            {
                'mail_message': Post.objects.latest("id"),
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{Post.objects.latest("id").title}',  # тема письма - заголовок поста
            body=f'{Post.objects.latest("id").preview()}',  # сообщение в письме
            from_email='a.v.lysenkov@yandex.ru',  # почта, с которой отправляется письмо
            to=email_list,  # список получателей
        )
        msg.attach_alternative(html_content, "text/html")  # добавление html
        msg.send()  # отсылка
        return redirect(f'/news/{Post.objects.latest("id").id}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверяем количество постов автора за текущие сутки
        limit = settings.DAILY_POST_LIMIT
        context['limit'] = limit
        last_day = timezone.now() - timedelta(days=1)
        posts_day_count = Post.objects.filter(
            author__user_link=self.request.user,
            time_add__gte=last_day,
        ).count()
        # context['count'] = posts_day_count
        context['can_create'] = posts_day_count < limit

        return context


# Представление для изменения поста с проверкой прав (форма и шаблон как для создания поста)
class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление для удаления поста
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')  # после удаления перенаправляем на страницу со списком постов


# Функция-представление для подписки на категорию постов
@login_required()
def subscribe_me(request, **kwargs):
    category_id = int(kwargs['pk'])
    user = request.user
    Category.objects.get(pk=category_id).subscribers.add(user)
    return redirect('/news/')


# Функция-представление для отписки от категории постов
@login_required()
def unsubscribe_me(request, **kwargs):
    category_id = int(kwargs['pk'])
    user = request.user
    Category.objects.get(pk=category_id).subscribers.remove(user)
    return redirect('/news/')