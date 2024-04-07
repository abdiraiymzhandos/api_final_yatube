from django.urls import path
from .views import FollowCreateView, GroupList, GroupCreate, ListCreateCommentsView, CommentDetailView

urlpatterns = [
    path('v1/follow/', FollowCreateView.as_view(), name='v1-follow-listcreate'),
    path('v1/groups/', GroupList.as_view(), name='v1-group-list'),
    path('v1/groups/create/', GroupCreate.as_view(), name='v1-group-create'),
    path('v1/posts/<int:post_id>/comments/', ListCreateCommentsView.as_view(), name='v1-comment-list-create'),
    path('v1/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='v1-comment-detail'),
]
