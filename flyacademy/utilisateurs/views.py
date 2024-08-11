# utilisateurs/views.py

from rest_framework import viewsets
from .models import Administrateur, Ambassadeur
from .serializers import AdministrateurSerializer, AmbassadeurSerializer

class AdministrateurViewSet(viewsets.ModelViewSet):
    queryset = Administrateur.objects.all()
    serializer_class = AdministrateurSerializer

class AmbassadeurViewSet(viewsets.ModelViewSet):
    queryset = Ambassadeur.objects.all()
    serializer_class = AmbassadeurSerializer
