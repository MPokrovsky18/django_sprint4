from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedCreatedModel
from blog.constants import CHARFIELDS_MAX_LENGTH, MAX_CHAR_LENGTH_TO_STR


User = get_user_model()


class Category(PublishedCreatedModel):
    """Model Thematic category."""

    title = models.CharField(
        'Заголовок',
        max_length=CHARFIELDS_MAX_LENGTH,
    )
    description = models.TextField('Описание',)
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta(PublishedCreatedModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:MAX_CHAR_LENGTH_TO_STR]


class Location(PublishedCreatedModel):
    """Model Geographic label."""

    name = models.CharField(
        'Название места',
        max_length=CHARFIELDS_MAX_LENGTH,
    )

    class Meta(PublishedCreatedModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:MAX_CHAR_LENGTH_TO_STR]


class Post(PublishedCreatedModel):
    """Model Post."""

    title = models.CharField(
        'Заголовок',
        max_length=CHARFIELDS_MAX_LENGTH,
    )
    text = models.TextField('Текст',)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        default_related_name = 'posts'
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:MAX_CHAR_LENGTH_TO_STR]
