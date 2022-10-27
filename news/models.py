from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.shortcuts import redirect


class Author(models.Model):  # класс авторов постов
    rating_author = models.IntegerField(default=0)  # рейтинг автора
    # cвязь один к одному с встроенной моделью пользователей User
    user_link = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):  # обновление рейтинга автора
        # суммарный рейтинг всех статей автора
        posts_rating = self.post_set.aggregate(posts_sum_rating=Sum('rating_post'))
        posts_rating_result = 0
        posts_rating_result += posts_rating.get('posts_sum_rating')

        # суммарный рейтинг всех комментариев автора
        com_aut_rating = self.user_link.comment_set.aggregate(com_aut_sum=Sum('rating_comment'))
        com_aut_result = 0
        com_aut_result += com_aut_rating.get('com_aut_sum')

        # суммарный рейтинг всех комментариев к статьям автора
        com_post_result = 0
        posts_author = self.post_set.all()  # выбираем все статьи автора
        # в цикле собираем все рейтинги комментариев по каждой статье автора
        for i in posts_author:
            com_post_rating = i.comment_set.aggregate(com_post_sum=Sum('rating_comment'))
            com_post_result += com_post_rating.get('com_post_sum')

        # расчет суммарного рейтинга автора и запись в базу данных
        self.rating_author = (3 * posts_rating_result) + com_aut_result + com_post_result
        self.save()
        pass

    def __str__(self):
        return f'{self.user_link.username}'


class Category(models.Model):  # класс категорий (тем) постов
    name = models.CharField(max_length=255, unique=True)  # название категории
    subscribers = models.ManyToManyField(User, through='CategoryUser')  # связь многие ко многим с пользователями

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):  # класс постов

    news = 'NE'
    article = 'AR'

    TYPE_CHOICE = [
        (news, 'news'),
        (article, 'article'),
    ]

    type_post = models.CharField(max_length=2, choices=TYPE_CHOICE, default=news)  # тип поста
    time_add = models.DateTimeField(auto_now_add=True)  # дата и время создания
    title = models.CharField(max_length=255)  # заголовок
    text = models.TextField(max_length=10000)  # текст поста
    rating_post = models.IntegerField(default=0)  # рейтинг поста
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь один ко многим с автором
    categories = models.ManyToManyField(Category, through='PostCategory')  # связь многие ко многим с категориями

    def like(self):  # увеличение рейтинга после лайка
        self.rating_post += 1
        self.save()

    def dislike(self):  # уменьшение рейтинга после дизлайка
        self.rating_post -= 1
        self.save()

    def preview(self):  # предпросмотр поста
        return self.text[0:50] + '...'

    def __str__(self):
        return f'{self.title.title()}: {self.preview()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):  # промежуточный класс для реализации связи многие ко многим
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь один ко многим с постом
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь один ко многим с категорией

    def __str__(self):
        return f'{self.post.preview()}: {self.category.name}'


class CategoryUser(models.Model):  # промежуточный класс для реализации связи многие ко многим
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь один ко многим с пользователем
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь один ко многим с категорией

    def __str__(self):
        return f'{self.user.username}: {self.category.name}'


class Comment(models.Model):  # класс комментариев к постам
    text = models.TextField(max_length=1000)  # текст комментария
    time_add = models.DateTimeField(auto_now_add=True)  # дата и время создания комментария
    rating_comment = models.IntegerField(default=0)  # рейтинг комментария
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь один ко многим с постом
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь один ко многим с пользователем

    def like(self):  # увеличение рейтинга после лайка
        self.rating_comment += 1
        self.save()

    def dislike(self):  # уменьшение рейтинга после дизлайка
        self.rating_comment -= 1
        self.save()

    def __str__(self):
        return f'{self.text[:19]}...'
