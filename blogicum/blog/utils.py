from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def base_queryset(model_manager=Post.objects,
                  author_request=False, comment_count_annotate=False):
    if author_request:
        query = model_manager.select_related('author', 'location', 'category')
    else:
        query = model_manager.select_related(
            'author', 'location', 'category').filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True)
    if comment_count_annotate:
        query = query.annotate(comment_count=Count('comments'))
    return query


def paginator_page_obj(posts, page_number):
    paginator = Paginator(posts, settings.POST_PER_PAGE)
    return paginator.get_page(page_number)
