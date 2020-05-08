__author__ = "aki"

from rest_framework.pagination import PageNumberPagination


# used to return total count, next and previous records link
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000