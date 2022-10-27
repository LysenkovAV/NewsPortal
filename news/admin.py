from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory, CategoryUser


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user_link', 'rating_author']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'type_post', 'time_add', 'author', 'rating_post']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(CategoryUser)
