from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PagePagination(PageNumberPagination):
    """Кастомна пагінація з розширеною мета-інформацією."""

    page_size = 10
    max_page_size = 100
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        """
        Перевизначає стандартну відповідь пагінації.
        Додає загальну кількість, кількість сторінок та посилання.
        """
        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'prev': bool(self.get_previous_link()),
            'next': bool(self.get_next_link()),
            'data': data
        })