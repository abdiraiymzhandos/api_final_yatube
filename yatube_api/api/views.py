from django.shortcuts import get_object_or_404
from rest_framework import filters

from .serializers import FollowSerializer, GroupSerializer, PostSerializer
from .serializers import CommentSerializer
from posts.models import Post, Group

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAuthenticatedAndAuthorOrReadOnly


class FollowListView(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return self.request.user.follows.all()


class PostViewSet(viewsets.ModelViewSet):
    """Представление для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedAndAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Выполняет создание новой записи."""
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Представление для работы с группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для работы с комментариями к постам."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedAndAuthorOrReadOnly]

    def get_queryset(self):
        """Ensure the post exists and return comments for it."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
