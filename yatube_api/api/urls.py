from .views import CommentViewSet, GroupViewSet, PostViewSet, FollowListView

from django.urls import path, include
from rest_framework.routers import DefaultRouter


router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='post')
router_v1.register('groups', GroupViewSet, basename='group')
router_v1.register('follow', FollowListView, basename='follow')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='v1-post-comments')

v1_urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/', include((v1_urlpatterns, 'api'), namespace='v1')),
]
