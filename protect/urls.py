from django.urls import path
from .views import (
    IndexView, AuthorEdit
)
from .views import upgrade_me


urlpatterns = [
    path('', IndexView.as_view()),
    path('profile/<int:pk>/edit/', AuthorEdit.as_view(), name='author_edit'),
    path('upgrade/', upgrade_me, name='upgrade'),
]