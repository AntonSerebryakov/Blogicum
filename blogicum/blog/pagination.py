from django.conf import settings
from django.core.paginator import Paginator


def paginator_page_obj(posts, page_number):
    paginator = Paginator(posts, settings.POST_PER_PAGE)
    return paginator.get_page(page_number)
