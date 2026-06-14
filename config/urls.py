from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('tickets.urls')),
    path('api/', include('faq.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path(
        'dashboard/employee/',
        TemplateView.as_view(template_name='employee_dashboard.html'),
        name='employee-dashboard',
    ),
    path(
        'dashboard/agent/',
        TemplateView.as_view(template_name='agent_dashboard.html'),
        name='agent-dashboard',
    ),
    path(
        'dashboard/admin/',
        TemplateView.as_view(template_name='admin_dashboard.html'),
        name='admin-dashboard',
    ),
    path(
        'tickets/create/',
        TemplateView.as_view(template_name='create_ticket.html'),
        name='create-ticket',
    ),
    path(
        'tickets/my/',
        TemplateView.as_view(template_name='my_tickets.html'),
        name='my-tickets',
    ),
    path(
        'tickets/<int:pk>/',
        TemplateView.as_view(template_name='ticket_detail.html'),
        name='ticket-detail-page',
    ),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq-page'),
    path(
        'users/',
        TemplateView.as_view(template_name='user_management.html'),
        name='user-management',
    ),
    path(
        'reports/',
        TemplateView.as_view(template_name='reports.html'),
        name='reports',
    ),
]
