from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from core.models import PublishedModel

TITLE_MAX_LENGTH = 256


User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
        verbose_name='Идентификатор'
    )

    def __str__(self):
        return (
            f'Категория публикаций {self.title[0:14]}, '
            f'описание {self.description[:14]}, '
            f'идентификатор {self.slug}.'
        )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishedModel):
    name = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Название места'
    )

    def __str__(self):
        return (f'Место публикации {self.name}.')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(PublishedModel):
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        ),
        verbose_name='Дата и время публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    def __str__(self):
        return (
            f'Публикация с заголовком {self.title[:14]}, '
            f'текст публикации {self.text[:14]}, '
            f'дата публикации {self.pub_date}, '
            f'автор публикации {self.author}, '
            f'местоположение {self.location}, '
            f'категория {self.category}.'
        )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)


class Comment(models.Model):
    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_author',
    )

    def __str__(self):
        return (
            f'Комментарий {self.text[:14]}, '
            f'к посту id{self.post__pk}, '
            f'автор комментария {self.author}, '
        )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('created_at',)
