from django import forms
from news.models import Author
from django.contrib.auth.models import User

# Для кастомизации формы регистрации из пакета allauth
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# Форма редактирования профиля
class AuthorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

# Кастомизация формы из пакета allauth
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
