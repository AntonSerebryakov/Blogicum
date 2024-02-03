from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required

from django.db.models import Count

from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from blog.models import Post, Category, Comment
from blog.forms import PostForm, CommentForm
from django.core.paginator import Paginator


POST_PER_INDEX_PAGE = 10


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


def base_queryset():
    return (Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True))


def index(request):
    posts = base_queryset().annotate(comment_count=Count('comments'))
    paginator = Paginator(posts, POST_PER_INDEX_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request, 'blog/index.html',
        {'page_obj': page_obj}
    )


def post_detail(request, post_id):
    context = {'post': get_object_or_404(base_queryset(), pk=post_id)}
    context['form'] = CommentForm()
    context['comments'] = Comment.objects.select_related(
        'author', 'post').filter(post__pk=post_id)
    return render(
        request,
        'blog/detail.html', context
    )


def edit_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id, author=request.user)
    form = CommentForm(request.POST or None, instance=instance)
    context = {'form': form}
    context['comment'] = Comment.objects.select_related(
        'author', 'post').get(pk=comment_id, post__id=post_id)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    return render(
        request,
        'blog/comment.html', context
    )


def delete_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id, author=request.user)
    form = CommentForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/comment.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = base_queryset().filter(
        category__slug=category_slug).annotate(
            comment_count=Count('comments'))
    paginator = Paginator(posts, POST_PER_INDEX_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html',
                  {'category': category,
                   'page_obj': page_obj})


def create(request, post_id=None):
    
    if post_id is not None:
        instance = get_object_or_404(Post, pk=post_id)
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id)
    else:
        instance = None
    if request.user.is_authenticated:
        form = PostForm(request.POST or None,
                        files=request.FILES or None, instance=instance)
        context = {'form': form}
        if form.is_valid():
            form_instance = form.save(commit=False)
            user = request.user
            form_instance.author = user
            form_instance.save()
            return redirect('blog:profile', user.get_username())
    else:
        return redirect('login')
    return render(request, 'blog/create.html', context)


def delete(request, post_id):
    instance = get_object_or_404(Post, pk=post_id, author=request.user)
    post = PostForm(instance=instance)
    context = {'post': post}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:posts')
    return render(request, 'blog/create.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {'profile': user}
    if user == request.user:
        posts = Post.objects.order_by(
            'pub_date').filter(
                author__username=username).annotate(
                    comment_count=Count('comments'))
    else:
        posts = base_queryset().order_by(
            'pub_date').filter(
                author__username=username).annotate(
                    comment_count=Count('comments'))
    paginator = Paginator(posts, POST_PER_INDEX_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, 'blog/profile.html', context)


@login_required(login_url='/auth/login/')
def edit_profile(request):
    name = request.user.get_username()
    user_instance = get_object_or_404(User, username=name)
    form = CustomUserChangeForm(request.POST, instance=user_instance)
    if form.is_valid():
        form.save()
        pass
    return render(request, 'blog/user.html', {'form': form})


@login_required(login_url='/auth/login/')
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id)
