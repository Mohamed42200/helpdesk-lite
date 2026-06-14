from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.permissions import IsAdmin

from .models import FAQ
from .serializers import FAQSerializer


class FAQListCreateView(generics.ListCreateAPIView):
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = FAQ.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(question__icontains=search) | Q(answer__icontains=search),
            )
        return queryset


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdmin()]
