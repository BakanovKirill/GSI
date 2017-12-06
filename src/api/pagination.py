from rest_framework import pagination
from rest_framework.response import Response

from gsi.settings import REST_FRAMEWORK


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        division = int(self.page.paginator.count) / REST_FRAMEWORK['PAGE_SIZE']
        remainder_division = int(self.page.paginator.count) % REST_FRAMEWORK['PAGE_SIZE']
        count_page = division + 1 if remainder_division else division

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'pages': count_page,
            'results': data
        })
