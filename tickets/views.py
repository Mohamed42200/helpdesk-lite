from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.permissions import IsAdmin, IsAdminOrAgent

from .models import Comment, Ticket
from .notifications import (
    send_comment_email,
    send_status_update_email,
    send_ticket_created_email,
    send_ticket_resolved_email,
)
from .serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    TicketCreateSerializer,
    TicketSerializer,
    TicketStatusSerializer,
)


class TicketCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save(created_by=request.user)
        send_ticket_created_email(ticket)
        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED,
        )


class MyTicketsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user():
            return Ticket.objects.all()
        if user.is_agent():
            return Ticket.objects.filter(assigned_to=user)
        return Ticket.objects.filter(created_by=user)


class AllTicketsView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.all()
        status_filter = self.request.query_params.get('status')
        priority_filter = self.request.query_params.get('priority')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        return queryset


class TicketDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user():
            return Ticket.objects.all()
        if user.is_agent():
            return Ticket.objects.filter(assigned_to=user)
        return Ticket.objects.filter(created_by=user)


class TicketStatusUpdateView(APIView):
    permission_classes = [IsAdminOrAgent]

    def patch(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response(
                {'detail': 'Ticket not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if ticket.is_closed():
            return Response(
                {'detail': 'Closed tickets cannot be modified.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        if user.is_agent() and ticket.assigned_to != user:
            return Response(
                {'detail': 'You can only update assigned tickets.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        old_status = ticket.get_status_display()
        serializer = TicketStatusSerializer(
            ticket, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if old_status != ticket.get_status_display():
            send_status_update_email(ticket, old_status)
        if ticket.status == Ticket.Status.RESOLVED:
            send_ticket_resolved_email(ticket)

        return Response(TicketSerializer(ticket).data)


class TicketCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response(
                {'detail': 'Ticket not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if ticket.is_closed():
            return Response(
                {'detail': 'Closed tickets cannot be modified.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        if user.is_admin_user():
            pass
        elif user.is_employee() and ticket.created_by != user:
            return Response(
                {'detail': 'You can only comment on your own tickets.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        elif user.is_agent() and ticket.assigned_to != user:
            return Response(
                {'detail': 'You can only comment on assigned tickets.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = Comment.objects.create(
            ticket=ticket,
            author=user,
            message=serializer.validated_data['message'],
        )
        send_comment_email(ticket, comment)
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )


class TicketCloseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response(
                {'detail': 'Ticket not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user
        if not user.is_employee() or ticket.created_by != user:
            return Response(
                {'detail': 'Only the ticket creator can close it.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if ticket.is_closed():
            return Response(
                {'detail': 'Ticket is already closed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_status = ticket.get_status_display()
        ticket.status = Ticket.Status.CLOSED
        ticket.save()
        send_status_update_email(ticket, old_status)
        return Response(TicketSerializer(ticket).data)


class ReportsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            'total_tickets': Ticket.objects.count(),
            'open_tickets': Ticket.objects.filter(
                status=Ticket.Status.OPEN,
            ).count(),
            'in_progress_tickets': Ticket.objects.filter(
                status=Ticket.Status.IN_PROGRESS,
            ).count(),
            'resolved_tickets': Ticket.objects.filter(
                status=Ticket.Status.RESOLVED,
            ).count(),
            'closed_tickets': Ticket.objects.filter(
                status=Ticket.Status.CLOSED,
            ).count(),
            'by_priority': {
                'low': Ticket.objects.filter(priority=Ticket.Priority.LOW).count(),
                'medium': Ticket.objects.filter(priority=Ticket.Priority.MEDIUM).count(),
                'high': Ticket.objects.filter(priority=Ticket.Priority.HIGH).count(),
            },
        })
