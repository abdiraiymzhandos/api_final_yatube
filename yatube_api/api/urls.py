from .views import CommentDetailView, FollowListView, PostListView
from .views import GroupList, GroupCreate, ListCreateCommentsView
from .views import PostDetailView, GroupDetailView

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)


urlpatterns = [
    path('v1/follow/', FollowListView.as_view(), name='follow-list'),
    path('v1/groups/', GroupList.as_view(), name='v1-group-list'),
    path('v1/groups/create/', GroupCreate.as_view(), name='v1-group-create'),
    path('v1/groups/<int:pk>/',
         GroupDetailView.as_view(), name='v1-group-detail'),
    path('v1/posts/<int:post_id>/comments/',
         ListCreateCommentsView.as_view(), name='v1-comment-list-create'),
    path('v1/posts/<int:post_id>/comments/<int:pk>/',
         CommentDetailView.as_view(), name='v1-comment-detail'),
    path('v1/jwt/create/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/posts/', PostListView.as_view(), name='post-list'),
    path('v1/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
