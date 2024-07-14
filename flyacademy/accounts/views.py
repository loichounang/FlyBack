# accounts/views.py
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout, login
from rest_framework.permissions import AllowAny

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)  # Connexion de l'utilisateur
        return Response({
            'token': user.auth_token.key,
            'user_id': user.pk,
            'username': user.username,
        })

class Logout(APIView):
    def post(self, request, format=None):
        logout(request)  # Déconnexion de l'utilisateur
        return Response(status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permet à tous les utilisateurs non authentifiés d'accéder à cette vue

