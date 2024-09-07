# messagerie/views.py

from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # S'assurer que l'utilisateur est authentifié

    @action(detail=False, methods=['get'], url_path='non-lus')
    def messages_non_lus(self, request):
        # Récupérer l'utilisateur connecté
        utilisateur_connecte = request.user
        
        # Filtrer les messages non lus pour cet utilisateur
        messages_non_lus = Message.objects.filter(destinataire=utilisateur_connecte, read_or_not=False)
        
        # Sérialiser les résultats
        serializer = self.get_serializer(messages_non_lus, many=True)
        
        return Response(serializer.data)

