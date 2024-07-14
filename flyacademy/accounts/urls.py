from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomAuthToken, Logout

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),  # Endpoint pour l'authentification
    path('api-token-logout/', Logout.as_view(), name='api_token_logout'),  # Endpoint pour la déconnexion
    # Autres URLs spécifiques à l'application 'accounts'
]
