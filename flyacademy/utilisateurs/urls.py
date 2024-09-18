# utilisateurs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UtilisateurViewSet, LogoutView, SessionManagement, RoleViewSet, CustomTokenObtainPairView, UserDetailView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
) 

router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet)
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='api_token_auth'),
    path('token/refresh', TokenRefreshView.as_view(), name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('session/', SessionManagement.as_view(), name='session_management'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
]
