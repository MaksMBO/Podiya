from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EventPagination(PageNumberPagination):
    """
    Custom pagination class for events.
    """
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        """
        Generates a paginated response for the queryset.
        """
        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
            'results': data,
        })
