from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now

from core.models import CreatedAt, PublishedCreatedModel
from blog.constants import CHARFIELDS_MAX_LENGTH, MAX_CHAR_LENGTH_TO_STR


class PostQuerySet(models.QuerySet):
    def select_related_fields(self):
        return self.select_related(
            'category',
            'location',
            'author',
        )

    def filter_is_published(self):
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now(),
        )

    def with_comment_count(self):
        return (
            self.annotate(comment_count=models.Count('comments'))
            .order_by('-pub_date')
        )


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
    image = models.ImageField(
        'Изображение',
        blank=True,
        upload_to='posts_images',
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
    objects = PostQuerySet.as_manager()

    class Meta:
        default_related_name = 'posts'
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:MAX_CHAR_LENGTH_TO_STR]

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(CreatedAt):
    """Model Comment."""

    text = models.TextField('Текст',)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta(CreatedAt.Meta):
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:MAX_CHAR_LENGTH_TO_STR]
