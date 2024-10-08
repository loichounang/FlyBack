# utilisateurs/views.py

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from .models import Utilisateur
from .serializers import UtilisateurSerializer, LoginSerializer, CustomTokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        token = data.get('access')

        # Récupérer l'utilisateur associé au token
        try:
            user = Utilisateur.objects.get(auth_token=token)
            user_data = UtilisateurSerializer(user).data
            data.update(user_data)
        except Utilisateur.DoesNotExist:
            pass

        return Response(data, status=status.HTTP_200_OK)
    
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UtilisateurSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return Utilisateur.objects.get(id=user.id)

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nom', 'email', 'role']
    search_fields = ['nom', 'email']
    ordering_fields = ['date_joined']

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def désactiver(self, request, pk=None):
        """Désactiver un utilisateur"""
        utilisateur = self.get_object()
        utilisateur.is_active = False
        utilisateur.save()
        return Response({'status': 'Utilisateur désactivé'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def get_admins(self, request, pk=None):
        """ Filter les administrateurs """
        queryset = self.queryset.filter(role='administrateur')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def réactiver(self, request, pk=None):
        """Réactiver un utilisateur désactivé"""
        utilisateur = self.get_object()
        utilisateur.is_active = True
        utilisateur.save()
        return Response({'status': 'Utilisateur réactivé'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def désactivés(self, request):
        """Lister tous les utilisateurs désactivés"""
        queryset = self.queryset.filter(is_active=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def changer_mot_de_passe(self, request, pk=None):
        """Changer le mot de passe de l'utilisateur"""
        utilisateur = self.get_object()
        new_password = request.data.get('new_password')
        if not new_password:
            raise ValidationError({"new_password": "Ce champ est requis."})
        utilisateur.set_password(new_password)
        utilisateur.save()
        return Response({'status': 'Mot de passe modifié avec succès'}, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = LoginSerializer  # Utilise le serializer mis à jour

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # Récupère l'utilisateur depuis les données validées
        user.statut = 'actif'
        user.dernier_accès = timezone.now()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"message": "Bienvenue dans votre espace personnel " + user.role,
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role,
            'status': user.statut,
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Obtenir le refresh token depuis la requête
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            
            # Mettre le token sur liste noire
            token.blacklist()

            # Optionnel: Changer le statut de l'utilisateur
            request.user.statut = "inactif"
            request.user.save()

            return Response({"message": "Logout succeeded"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SessionManagement(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        last_login = user.last_login
        session_timeout = settings.SESSION_TIMEOUT
        if timezone.now() - last_login > timezone.timedelta(minutes=session_timeout):
            logout(request)
            return Response({"detail": "Session expired. You have been logged out."},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response({"detail": "Session is active."})


class RoleViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def list_roles(self, request):
        roles = dict(Utilisateur.ROLE_CHOICES)  # Convertit les choix en un dictionnaire
        return Response(roles)