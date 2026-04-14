from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

User = get_user_model()


def get_paginated_posts(queryset, request, per_page=10):
    """Возвращает отпагинированный список постов."""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category', 'location'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')
    page = get_paginated_posts(post_list, request)
    context = {
        'page': page,
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('category', 'location'),
        pk=pk
    )
    if (
        post.pub_date > timezone.now()
        or not post.is_published
        or (post.category and not post.category.is_published)
    ):
        if request.user != post.author:
            raise get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author').all()
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': comments,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related(
        'location'
    ).filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True
    ).order_by('-pub_date')
    page = get_paginated_posts(post_list, request)
    context = {
        'category': category,
        'page': page,
    }
    return render(request, template, context)


@login_required
def create_post(request):
    template = 'blog/create.html'
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, template, context)


@login_required
def edit_post(request, pk):
    template = 'blog/create.html'
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('blog:post_detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, template, context)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('blog:post_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form, 'post': comment.post, 'comment': comment}
    return render(request, 'blog/edit_comment.html', context)


@login_required
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=pk)
    context = {'comment': comment}
    return render(request, 'blog/edit_comment.html', context)


def profile(request, username):
    template = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    if request.user == user:
        post_list = user.posts.all()
    else:
        post_list = user.posts.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    post_list = post_list.select_related('category', 'location').order_by('-pub_date')
    page = get_paginated_posts(post_list, request)
    context = {
        'user': user,
        'page': page,
    }
    return render(request, template, context)
