# utilisateurs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UtilisateurViewSet, CustomAuthToken, LogoutView, SessionManagement, RoleViewSet
router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet)
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('session/', SessionManagement.as_view(), name='session_management'),
]
