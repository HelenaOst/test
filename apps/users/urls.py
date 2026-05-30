from django.urls import path

from apps.users.views import (
    UserBlockView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserMeDeleteView,
    UserMeUpdateView,
    UserMeView,
    UserToManagerView,
)

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('users/me/', UserMeView.as_view()),
    path('users/me/update/', UserMeUpdateView.as_view()),
    path('users/me/delete/', UserMeDeleteView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/<int:pk>/delete/', UserDeleteView.as_view()),
    path('users/<int:pk>/block/', UserBlockView.as_view()),
    path('users/<int:pk>/manager/', UserToManagerView.as_view()),
]
