from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from posts.models import Follow, Group
from .serializers import FollowSerializer, GroupSerializer
from posts.models import Comment, Post, Follow, Group
from .serializers import CommentSerializer
from django.shortcuts import get_object_or_404

class FollowListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

class FollowCreateView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        following = serializer.validated_data['following']
        if following == request.user:
            return Response({"error": "Нельзя подписаться на самого себя!"}, status=status.HTTP_400_BAD_REQUEST)
        elif Follow.objects.filter(user=request.user, following=following).exists():
            return Response({"error": "Вы уже подписаны на этого пользователя."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupList(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GroupCreate(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListCreateCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        This view returns a list of all comments for
        the post as determined by the post_id portion of the URL.
        """
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        """
        Override perform_create to associate the comment with the correct post
        using the post_id URL parameter and to set the comment's author to the current user.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)  # Ensure the post exists
        serializer.save(author=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all comments for
        the comment as determined by the post_id portion of the URL.
        """
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response({"error": "You can only delete your own comments."}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
