# cours/views.py

from rest_framework import viewsets
from .models import Catégorie, Cours, Chapitre, Leçon, Quizz
from .serializers import CatégorieSerializer, CoursSerializer, ChapitreSerializer, LeçonSerializer, QuizzSerializer

class CatégorieViewSet(viewsets.ModelViewSet):
    queryset = Catégorie.objects.all()
    serializer_class = CatégorieSerializer

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer

class ChapitreViewSet(viewsets.ModelViewSet):
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer

class LeçonViewSet(viewsets.ModelViewSet):
    queryset = Leçon.objects.all()
    serializer_class = LeçonSerializer

class QuizzViewSet(viewsets.ModelViewSet):
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer
