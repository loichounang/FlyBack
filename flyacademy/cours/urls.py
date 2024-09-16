# cours/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CatégorieViewSet, CoursViewSet, ChapitreViewSet, LeçonViewSet, QuizzViewSet, ListCategoriesWithInfos, RatingViewSet, ListChaptersByCourseIdView

router = DefaultRouter()
router.register(r'categories', CatégorieViewSet)
router.register(r'cours', CoursViewSet)
router.register(r'chapitres', ChapitreViewSet)
router.register(r'leçons', LeçonViewSet)
router.register(r'quizz', QuizzViewSet)
router.register(r'ratings', RatingViewSet, basename='rating')


urlpatterns = [
    path('', include(router.urls)),
    path('categories/list-all', ListCategoriesWithInfos.as_view(), name='categories-without-value'),
    path('chapitre/', ListChaptersByCourseIdView.as_view(), name='list-chapter-by-course-id'),
]
