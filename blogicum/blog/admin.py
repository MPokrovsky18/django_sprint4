from django.contrib import admin
from django.contrib.auth.models import Group

from blog.models import Category, Location, Post, Comment


admin.site.unregister(Group)
admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'created_at',
        'pub_date',
        'author',
        'location',
        'category',
    )
    list_editable = (
        'is_published',
        'pub_date',
        'category',
    )
    search_fields = ('title',)
    list_filter = (
        'category',
        'location',
    )
    date_hierarchy = 'pub_date'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_filter = ('is_published',)
    inlines = (PostInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'slug',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    inlines = (PostInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'created_at',
        'author',
    )
    search_fields = ('text',)
    date_hierarchy = 'created_at'
