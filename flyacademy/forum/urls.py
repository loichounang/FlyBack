# cours/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SujetViewSet, RéponseViewSet

router = DefaultRouter()
router.register(r'sujet', SujetViewSet)
router.register(r'reponse', RéponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
