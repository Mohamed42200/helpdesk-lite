from django.urls import path

from .views import (
    AgentListView,
    LoginView,
    RegisterView,
    UserDetailView,
    UserListCreateView,
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('users', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('agents', AgentListView.as_view(), name='agent-list'),
]
