from django.utils.timezone import now
from django.shortcuts import get_object_or_404, render

from blog.models import Category, Post
from blog.constants import MAX_POSTS_COUNT_ON_PAGE


def get_filtered_posts(posts_manager):
    """
    Get QuerySet of Posts where pub_date < now,
    post is published, and category of posts is published.
    """
    return posts_manager.select_related(
        'category',
        'location',
        'author',
    ).filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    """Get homepage."""
    post_list = get_filtered_posts(
        Post.objects
    )[:MAX_POSTS_COUNT_ON_PAGE]

    return render(
        request,
        'blog/index.html',
        {'post_list': post_list},
    )


def post_detail(request, post_id: int):
    """Get detail info."""
    post = get_object_or_404(
        get_filtered_posts(Post.objects),
        pk=post_id,
    )

    return render(
        request,
        'blog/detail.html',
        {'post': post},
    )


def category_posts(request, category_slug: str):
    """Get posts by category."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': get_filtered_posts(category.posts)
        },
    )
