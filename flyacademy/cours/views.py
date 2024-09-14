# cours/views.py

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework import generics
from django.db.models import Count
from rest_framework.response import Response
from .models import Catégorie, Cours, Chapitre, Leçon, Quizz, CoursUtilisateur, Rating
from .serializers import CatégorieSerializer, CoursSerializer, ChapitreSerializer, LeçonSerializer, QuizzSerializer, CatégorieListSerializer, RatingSerializer

class RatingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cours_id = request.data.get('cours_id')
        score = request.data.get('score')

        if not cours_id or not score:
            return Response({'error': 'cours_id and score are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cours = Cours.objects.get(id=cours_id)
        except Cours.DoesNotExist:
            return Response({'error': 'Cours not found'}, status=status.HTTP_404_NOT_FOUND)

        rating, created = Rating.objects.get_or_create(user=request.user, cours=cours, defaults={'score': score})

        if not created:
            rating.score = score
            rating.save()

        # Update the course rating
        cours.update_rating()

        return Response({'message': 'Rating submitted successfully'}, status=status.HTTP_201_CREATED)

class CatégorieViewSet(viewsets.ModelViewSet):
    queryset = Catégorie.objects.all()
    serializer_class = CatégorieSerializer

class ListCategoriesWithInfos(generics.ListAPIView):
    queryset = Catégorie.objects.all()
    serializer_class = CatégorieListSerializer

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer

    # Action pour récupérer tous les cours commencés, indépendamment de l'utilisateur
    @action(detail=False, methods=['get'], url_path='tous-les-cours-commences')
    def tous_les_cours_commences(self, request):
        # Récupérer tous les enregistrements de Cours avec statut 'active'
        cours_commences = Cours.objects.filter(cours_status='active')
        # Extraire les identifiants de cours commencés
        cours_ids = cours_commences.values_list('id', flat=True)
        # Récupérer les cours correspondants
        cours = Cours.objects.filter(id__in=cours_ids)
        # Sérialiser les données des cours pour la réponse
        serializer = self.get_serializer(cours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Action pour récupérer les cours actifs de l'utilisateur connecté
    @action(detail=False, methods=['get'], url_path='actifs')
    def cours_actifs(self, request):
        utilisateur = request.user
        cours_actifs = CoursUtilisateur.objects.filter(utilisateur=utilisateur, statut='active')
        cours_ids = cours_actifs.values_list('cours', flat=True)
        cours = Cours.objects.filter(id__in=cours_ids)
        serializer = self.get_serializer(cours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Autres actions spécifiques pour les cours
    @action(detail=True, methods=['post'], url_path='commencer')
    def commencer_cours(self, request, pk=None):
        try:
            cours = self.get_object()
            utilisateur = request.user
            cours_utilisateur, created = CoursUtilisateur.objects.get_or_create(utilisateur=utilisateur, cours=cours, statut='active')
            if created:
                message = 'Cours démarré avec succès.'
            else:
                message = 'Vous avez déjà commencé ce cours.'
            return Response({'message': message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='terminer')
    def terminer_cours(self, request, pk=None):
        try:
            cours = self.get_object()
            utilisateur = request.user
            cours_utilisateur = CoursUtilisateur.objects.filter(utilisateur=utilisateur, cours=cours, statut='active').first()
            if cours_utilisateur:
                cours_utilisateur.statut = 'inactive'
                cours_utilisateur.save()
                message = 'Cours terminé avec succès.'
            else:
                message = 'Vous n\'avez pas encore commencé ce cours.'
            return Response({'message': message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ChapitreViewSet(viewsets.ModelViewSet):
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer

    def retrieve(self, request, *args, **kwargs):
        chapitre = self.get_object()
        leçons = Leçon.objects.filter(chapitre=chapitre)
        leçon_serializer = LeçonSerializer(leçons, many=True)
        data = {
            'chapitre': ChapitreSerializer(chapitre).data,
            'leçons': leçon_serializer.data
        }
        return Response(data)

class LeçonViewSet(viewsets.ModelViewSet):
    queryset = Leçon.objects.all()
    serializer_class = LeçonSerializer

class QuizzViewSet(viewsets.ModelViewSet):
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer
