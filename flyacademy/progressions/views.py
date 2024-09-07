from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Interactions
from rest_framework.authentication import TokenAuthentication
from .serializers import InteractionsSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interactions.objects.all()
    serializer_class = InteractionsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['utilisateur__username', 'type_interaction']
    ordering_fields = ['timestamp']
