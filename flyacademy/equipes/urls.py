# equipes/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipeViewSet

router = DefaultRouter()

router.register(r'equipes', EquipeViewSet)

urlpatterns = [
    path('', include(router.urls))
]