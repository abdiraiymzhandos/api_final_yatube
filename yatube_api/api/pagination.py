from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class ConditionalPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        if 'no_pagination' in request.query_params:
            return None  # Bypass pagination
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if 'no_pagination' in self.request.query_params:
            return Response(data)  # Return data directly without pagination
        return super().get_paginated_response(data)
