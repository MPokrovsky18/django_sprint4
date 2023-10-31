from django.db import models


class CreatedAt(models.Model):
    """Abstract model. Add creation time."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class PublishedCreatedModel(CreatedAt):
    """Absract model. Add creation time and flag is_published."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta(CreatedAt.Meta):
        abstract = True
