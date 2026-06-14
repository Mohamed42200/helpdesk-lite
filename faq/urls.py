from django.urls import path

from .views import FAQDetailView, FAQListCreateView

urlpatterns = [
    path('faq', FAQListCreateView.as_view(), name='faq-list-create'),
    path('faq/<int:pk>', FAQDetailView.as_view(), name='faq-detail'),
]
