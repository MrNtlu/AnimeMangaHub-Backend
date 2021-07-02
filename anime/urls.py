from django.urls import path, include
from anime import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('search', views.AnimeViewSet, basename='search_anime')

urlpatterns = [
    path('topList',views.getTopAnimeList, name='top_anime_list'),
    path('genre/<parameter>',views.getAnimeByGenre, name='anime_by_genre'),
    path('<parameter>',views.getAnime, name='anime_details'),
    path('', include(router.urls)),
]