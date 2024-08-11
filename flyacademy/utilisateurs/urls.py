# utilisateurs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdministrateurViewSet, AmbassadeurViewSet

router = DefaultRouter()
router.register(r'administrateurs', AdministrateurViewSet)
router.register(r'ambassadeurs', AmbassadeurViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
