from django.urls import path
from .views import (
    PostList, PostDetail, PostCreate, PostEdit, PostDelete, subscribe_me, unsubscribe_me
)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscribe/<int:pk>/', subscribe_me, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_me, name='unsubscribe'),
]