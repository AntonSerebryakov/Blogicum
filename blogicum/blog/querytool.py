from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def base_queryset(model_manager=Post.objects,
                  publicated_only=True,
                  comment_count_annotate=False,
                  order_by_pub_date_rev=False):
    query = model_manager.select_related('author', 'location', 'category')
    if publicated_only:
        query = query.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True)
    if comment_count_annotate:
        query = query.annotate(comment_count=Count('comments'))
    if order_by_pub_date_rev:
        query = query.order_by('-pub_date')
    return query
