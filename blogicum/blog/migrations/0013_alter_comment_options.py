# Generated by Django 3.2.16 on 2023-10-31 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_rename_publication_comment_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'default_related_name': 'comments', 'ordering': ('-created_at',), 'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
