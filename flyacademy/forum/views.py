# forum/views.py

from rest_framework import viewsets
from .models import SujetForum, MessageForum
from .serializers import SujetSerializer, RéponseSerializer

class SujetViewSet(viewsets.ModelViewSet):
    queryset = SujetForum.objects.all()
    serializer_class = SujetSerializer

class RéponseViewSet(viewsets.ModelViewSet):
    queryset = MessageForum.objects.all()
    serializer_class = RéponseSerializer
