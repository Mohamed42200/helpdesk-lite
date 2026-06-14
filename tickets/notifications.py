from django.core.mail import send_mail
from django.conf import settings


def _send(subject, message, recipient):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=True,
    )


def send_registration_email(user):
    _send(
        'Welcome to Helpdesk Lite',
        f'Hi {user.username},\n\nYour account has been created successfully.',
        user.email or f'{user.username}@example.com',
    )


def send_ticket_created_email(ticket):
    _send(
        f'Ticket Created: {ticket.title}',
        f'Your ticket #{ticket.id} has been created.\n\n'
        f'Title: {ticket.title}\n'
        f'Priority: {ticket.get_priority_display()}\n'
        f'Status: {ticket.get_status_display()}',
        ticket.created_by.email or f'{ticket.created_by.username}@example.com',
    )


def send_comment_email(ticket, comment):
    recipients = {ticket.created_by.email or f'{ticket.created_by.username}@example.com'}
    if ticket.assigned_to:
        recipients.add(
            ticket.assigned_to.email or f'{ticket.assigned_to.username}@example.com'
        )
    for recipient in recipients:
        _send(
            f'New comment on ticket #{ticket.id}',
            f'{comment.author.username} commented:\n\n{comment.message}',
            recipient,
        )


def send_status_update_email(ticket, old_status):
    _send(
        f'Ticket #{ticket.id} status updated',
        f'Status changed from {old_status} to {ticket.get_status_display()}.\n\n'
        f'Title: {ticket.title}',
        ticket.created_by.email or f'{ticket.created_by.username}@example.com',
    )


def send_ticket_resolved_email(ticket):
    _send(
        f'Ticket #{ticket.id} resolved',
        f'Your ticket "{ticket.title}" has been resolved.',
        ticket.created_by.email or f'{ticket.created_by.username}@example.com',
    )
