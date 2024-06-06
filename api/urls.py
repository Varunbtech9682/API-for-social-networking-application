from django.urls import path
from .views import SignupView, LoginView, UserSearchView, FriendRequestView, FriendRequestActionView, FriendListView, PendingFriendRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-requests/', FriendRequestView.as_view(), name='friend-requests'),
    path('friend-requests/action/', FriendRequestActionView.as_view(), name='friend-request-action'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('friend-requests/pending/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]
