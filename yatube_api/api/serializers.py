from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Follow, Group, User

# from rest_framework.validators import UniqueTogetherValidator
# from rest_framework.fields import CurrentUserDefault

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['user', 'following']


# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     following = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all()
#     )

#     class Meta:
#         model = Follow
#         fields = ['user', 'following']
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=['user', 'following'],
#                 message="Вы уже подписаны на этого пользователя."
#             )
#         ]

#     def validate_following(self, value):
#         """
#         Check that the user is not trying to follow themselves.
#         """
#         if value == self.context['request'].user:
#             raise serializers.ValidationError(
#                 "Нельзя подписаться на самого себя!")
#         return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
