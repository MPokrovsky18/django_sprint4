from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.http import Http404

from .models import Category, Post, Comment
from .forms import PostForm, CommentForm


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'blog/user.html'
    fields = (
        'username', 'first_name', 'last_name', 'email',
    )

    def get_object(self):
        user = self.request.user
        print(user)
        return user

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class UpdateDeleteCommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id=instance.post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpdateView(UpdateDeleteCommentMixin, UpdateView):
    pass


class CommentDeleteView(UpdateDeleteCommentMixin, DeleteView):
    pass


class CommentCreateView(LoginRequiredMixin, CreateView):
    publication = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.publication = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.publication
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.publication.pk}
        )


class PostGetMixin:
    model = Post

    def get_object(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id'],
        )

        if not post.is_published and post.author != self.request.user:
            raise Http404

        return post


class PostChangeMixin(LoginRequiredMixin):
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id=instance.pk)
        return super().dispatch(request, *args, **kwargs)


class PostDetailView(PostGetMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )

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


class PostUpdateView(PostChangeMixin, PostGetMixin, UpdateView):
    pass


class PostDeleteView(PostChangeMixin, PostGetMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class PostListMixin:
    model = Post
    paginate_by = 10
    apply_filters = True

    def get_filters(self):
        return {
            'pub_date__lte': now(),
            'is_published': True,
            'category__is_published': True
        }

    def get_posts(self, base_manager, **kwargs):
        return base_manager.select_related(
            'category', 'author', 'location'
        ).filter(
            **(self.get_filters() if self.apply_filters else kwargs)
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class PostListView(PostListMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        return self.get_posts(Post.objects)


class ProfilePostsListView(PostListMixin, ListView):
    template_name = 'blog/profile.html'
    profile = None

    def get_queryset(self):
        self.profile = get_object_or_404(
            get_user_model(), username=self.kwargs['username']
        )
        self.apply_filters = not self.profile == self.request.user

        return self.get_posts(self.profile.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class CategoryPostListView(PostListMixin, ListView):
    template_name = 'blog/category.html'
    category = None

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )
        return self.get_posts(self.category.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
