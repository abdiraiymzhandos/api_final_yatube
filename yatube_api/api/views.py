from rest_framework import generics, permissions, status, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from django.shortcuts import get_object_or_404

from .serializers import FollowSerializer, GroupSerializer, PostSerializer
from .serializers import CommentSerializer
from .permissions import IsAuthorOrReadOnly

from posts.models import Comment, Post, Follow, Group


class FollowListView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        search_username = self.request.query_params.get('search', None)
        if search_username:
            # Filter the queryset based on the username of the following user
            queryset = queryset.filter(following__username=search_username)
        return queryset

    def perform_create(self, serializer):
        # Access the currently authenticated user from the request
        user = self.request.user
        following = serializer.validated_data['following']

        # Check if the user is trying to follow themselves
        if following == user:
            raise serializers.ValidationError(
                {"error": "Нельзя подписаться на самого себя!"})

        # Check if the follow relationship already exists
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                {"error": "Вы уже подписаны на этого пользователя."})

        serializer.save(user=user)


class GroupList(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None


class GroupCreate(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupDetailView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListCreateCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)  # Ensure the post exists
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {"error": "You can only delete your own comments."},
                status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)


class PostListView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    ordering_fields = ('-pub_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
