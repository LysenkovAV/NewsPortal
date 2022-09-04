from django.shortcuts import render

from django.views.generic import (
    TemplateView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Author
import news.urls
from django.contrib.auth.models import User
from .forms import AuthorForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# Представление для редактирования профиля с проверкой
class AuthorEdit(LoginRequiredMixin, UpdateView):
    form_class = AuthorForm
    model = User
    template_name = 'protect/profile_edit.html'
    success_url = reverse_lazy('post_list')


# Представление для отображения информации аутентифицированным пользователям
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # True, если пользователь не находится в группе авторов
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


# Функция-представления для апгрейда аккаунта - добавление в группу авторов
@login_required()
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
