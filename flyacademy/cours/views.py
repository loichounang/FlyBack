# cours/views.py

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework import generics
from django.db.models import Count
from datetime import timezone
from rest_framework.response import Response
from .models import Catégorie, Cours, Chapitre, Leçon, Quizz, CoursUtilisateur, Rating, ProgressionLeçon
from .serializers import CatégorieSerializer, CoursSerializer, ChapitreSerializer, LeçonSerializer, QuizzSerializer, CatégorieListSerializer, RatingSerializer, ProgressionLeçonSerializer, CoursUtilisateursSerializer

class RatingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer

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
    parser_classes = [MultiPartParser]  # Ajout pour la gestion des fichiers multipart

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
    
class ListChaptersByCourseIdView(generics.ListAPIView):
    serializer_class = ChapitreSerializer

    def get_queryset(self):
        cours_id = self.request.query_params.get('coursId')
        if cours_id:
            return Chapitre.objects.filter(cours_id=cours_id)
        return Chapitre.objects.none()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'chapitres': serializer.data})

class LeçonViewSet(viewsets.ModelViewSet):
    queryset = Leçon.objects.all()
    serializer_class = LeçonSerializer
    parser_classes = [MultiPartParser]  # Ajout pour la gestion des fichiers multipart

class QuizzViewSet(viewsets.ModelViewSet):
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer

# Permettre à un utilisateur de s'enregistrer à un cours et suivre son évolution
class CoursUtilisateurViewSet(viewsets.ModelViewSet):
    queryset = CoursUtilisateur.objects.all()
    serializer_class = CoursUtilisateursSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        utilisateur = request.user
        cours_id = request.data.get('cours_id')

        try:
            cours = Cours.objects.get(id=cours_id)
        except Cours.DoesNotExist:
            return Response({"detail": "Cours non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur est déjà inscrit à ce cours
        cours_utilisateur, created = CoursUtilisateur.objects.get_or_create(utilisateur=utilisateur, cours=cours)

        if not created:
            return Response({"detail": "Vous êtes déjà inscrit à ce cours."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(cours_utilisateur)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# Gestion de la progression dans le suivi d'un cours
class ProgressionLeçonViewSet(viewsets.ModelViewSet):
    queryset = ProgressionLeçon.objects.all()
    serializer_class = ProgressionLeçonSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        progression = self.get_object()
        statut_leçon = request.data.get('statut_leçon')

        if statut_leçon not in ['not_started', 'in_progress', 'completed']:
            return Response({"detail": "Statut de leçon invalide."}, status=status.HTTP_400_BAD_REQUEST)

        progression.statut_leçon = statut_leçon

        # Si la leçon est complétée, enregistrer la date de fin
        if statut_leçon == 'completed':
            progression.date_terminée = timezone.now()

        progression.save()

        serializer = self.get_serializer(progression)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Lister les cours par catégorie
class CoursByCategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        category_id = request.query_params.get('category_id')
        if category_id is None:
            return Response({'detail': 'category_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            courses = Cours.objects.filter(categorie_id=category_id)
            serializer = CoursSerializer(courses, many=True)
            return Response(serializer.data)
        except Cours.DoesNotExist:
            return Response({'detail': 'Courses not found'}, status=status.HTTP_404_NOT_FOUND)