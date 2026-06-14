from django.urls import path

from .views import (
    AllTicketsView,
    MyTicketsView,
    ReportsView,
    TicketCloseView,
    TicketCommentView,
    TicketCreateView,
    TicketDetailView,
    TicketStatusUpdateView,
)

urlpatterns = [
    path('tickets', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/my', MyTicketsView.as_view(), name='ticket-my'),
    path('tickets/all', AllTicketsView.as_view(), name='ticket-all'),
    path('tickets/reports', ReportsView.as_view(), name='ticket-reports'),
    path('tickets/<int:pk>', TicketDetailView.as_view(), name='ticket-detail'),
    path(
        'tickets/<int:pk>/status',
        TicketStatusUpdateView.as_view(),
        name='ticket-status',
    ),
    path(
        'tickets/<int:pk>/comment',
        TicketCommentView.as_view(),
        name='ticket-comment',
    ),
    path(
        'tickets/<int:pk>/close',
        TicketCloseView.as_view(),
        name='ticket-close',
    ),
]
