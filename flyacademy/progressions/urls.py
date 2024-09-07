from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import InteractionViewSet

router = DefaultRouter()
router.register(r'interactions', InteractionViewSet, basename='interaction')

urlpatterns = [
    path('', include(router.urls)),
]
