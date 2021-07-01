from django.urls import path
from anime import views

urlpatterns = [
    path('topList',views.getTopAnimeList, name='top_anime_list'),
    path('genre/<parameter>',views.getAnimeByGenre, name='anime_by_genre'),
]