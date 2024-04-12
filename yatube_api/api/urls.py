from .views import CommentDetailView, FollowListView, PostListView
from .views import GroupList, GroupCreate, ListCreateCommentsView
from .views import PostDetailView, GroupDetailView

from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)

v1_urlpatterns = [
    path('follow/', FollowListView.as_view(), name='follow-list'),
    path('groups/', GroupList.as_view(), name='v1-group-list'),
    path('groups/create/', GroupCreate.as_view(), name='v1-group-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(),
         name='v1-group-detail'),
    path('posts/<int:post_id>/comments/', ListCreateCommentsView.as_view(),
         name='v1-comment-list-create'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(),
         name='v1-comment-detail'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('jwt/create/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns = [
    path('v1/', include((v1_urlpatterns, 'api'), namespace='v1')),
]

# path('jwt/', include('djoser.urls.jwt')), IT DOES NOT WORK
