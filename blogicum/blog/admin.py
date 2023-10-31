from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from blog.models import Category, Location, Post, Comment


admin.site.unregister(Group)
admin.site.empty_value_display = 'Не задано'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'post_image',
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
    inlines = (CommentInline,)

    @admin.display(description="Изображение")
    def post_image(self, obj):
        return (
            mark_safe(f'<img src={obj.image.url} width="80" height="60">')
            if obj.image
            else 'без изображения'
        )


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
