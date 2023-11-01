from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView
)

from .models import Category, Post
from .forms import PostForm, CommentForm
from .mixins import AuthorVerificationMixin, CommentMixin, PostMixin
from .constants import MAX_OBJECT_COUNT_ON_PAGE


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'blog/user.html'
    fields = (
        'username', 'first_name', 'last_name', 'email',
    )

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class CommentUpdateView(CommentMixin, AuthorVerificationMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, AuthorVerificationMixin, DeleteView):
    pass


class CommentCreateView(CommentMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class PostDetailView(ListView):
    template_name = 'blog/detail.html'
    paginate_by = MAX_OBJECT_COUNT_ON_PAGE
    post_data = None

    def get_post(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id'],
        )

        if not post.is_published and post.author != self.request.user:
            raise Http404

        return post

    def get_queryset(self):
        self.post_data = self.get_post()
        return self.post_data.comments.select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_post()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(PostMixin, UpdateView):
    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(PostMixin, DeleteView):
    pass


class PostListView(ListView):
    template_name = 'blog/index.html'
    paginate_by = MAX_OBJECT_COUNT_ON_PAGE

    def get_queryset(self):
        return (
            Post.objects
            .select_related_fields()
            .filter_is_published()
            .with_comment_count()
        )


class ProfilePostsListView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = MAX_OBJECT_COUNT_ON_PAGE
    author = None

    def get_author(self):
        return get_object_or_404(
            get_user_model(),
            username=self.kwargs['username']
        )

    def get_queryset(self):
        self.author = self.get_author()
        posts = (
            self.author.posts
            .select_related_fields()
            .with_comment_count()
        )
        if not self.author == self.request.user:
            posts = posts.filter_is_published()

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class CategoryPostListView(ListView):
    template_name = 'blog/category.html'
    paginate_by = MAX_OBJECT_COUNT_ON_PAGE
    category = None

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        self.category = self.get_category()
        return (
            self.category.posts
            .select_related_fields()
            .filter_is_published()
            .with_comment_count()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
