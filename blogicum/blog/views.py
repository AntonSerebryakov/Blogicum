from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView

from blog.models import Comment, Category, Post
from blog.forms import CustomUserChangeForm, CommentForm, PostForm
from blog.pagination import paginator_page_obj
from blog.querytool import base_queryset


class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')


def index(request):
    posts = base_queryset(
        comment_count_annotate=True,
        order_by_pub_date_rev=True)
    return render(
        request, 'blog/index.html',
        {'page_obj': paginator_page_obj(posts, request.GET.get('page'))}
    )


def post_detail(request, post_id):
    post = get_object_or_404(base_queryset(publicated_only=False), pk=post_id)
    if (post.author != request.user) and ((not post.is_published) or (
        not post.category.is_published) or (
            post.pub_date > timezone.now())):
        raise Http404
    context = {'post': post}
    context['form'] = CommentForm()
    context['comments'] = post.comments.all()
    return render(
        request,
        'blog/detail.html', context
    )


@login_required
def edit_comment(request, post_id, comment_id):
    instance = get_object_or_404(
        Comment.objects.select_related('author', 'post'),
        pk=comment_id, post__pk=post_id, author=request.user)
    form = CommentForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    return render(
        request,
        'blog/comment.html',
        {'form': form, 'comment': instance}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id, author=request.user)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/comment.html')


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = base_queryset(
        model_manager=category.posts,
        comment_count_annotate=True,
        order_by_pub_date_rev=True)
    return render(request, 'blog/category.html',
                  {'category': category,
                   'page_obj': paginator_page_obj(
                       posts, request.GET.get('page'))})


@login_required
def create_post(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    context = {'form': form}
    if form.is_valid():
        form_instance = form.save(commit=False)
        form_instance.author = request.user
        form_instance.save()
        return redirect('blog:profile', request.user.get_username())
    return render(request, 'blog/create.html', context)


@login_required
def edit_post(request, post_id):
    instance = get_object_or_404(
        base_queryset(publicated_only=False), pk=post_id)
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user.get_username())
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(
        base_queryset(publicated_only=False), pk=post_id, author=request.user)
    form = PostForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:posts')
    return render(request, 'blog/create.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {'profile': user}
    if user == request.user:
        posts = base_queryset(
            model_manager=user.posts,
            publicated_only=False,
            comment_count_annotate=True,
            order_by_pub_date_rev=True)
    else:
        posts = base_queryset(
            model_manager=user.posts,
            comment_count_annotate=True,
            order_by_pub_date_rev=True)
    context['page_obj'] = paginator_page_obj(posts, request.GET.get('page'))
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    user_instance = request.user
    form = CustomUserChangeForm(request.POST or None, instance=user_instance)
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id)
