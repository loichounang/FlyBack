# utilisateurs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UtilisateurViewSet, CustomAuthToken, LogoutView, SessionManagement
router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('session/', SessionManagement.as_view(), name='session_management'),
]
