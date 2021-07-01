from src.base_response import handleResponseMessage
from rest_framework import status
from rest_framework.decorators import api_view
from anime import serializers, models
from django.db.models import Avg
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage


ANIME_PAGINATION_LIMIT = 25


@api_view(['GET'])
def getTopAnimeList(request):
    if request.user.is_authenticated:
        animeList = models.AnimeModel.objects.annotate(
            avg_rating=Avg('anime_review__rating')
        ).order_by("-avg_rating")
        
        page = request.GET.get('page')
        paginator = Paginator(animeList, ANIME_PAGINATION_LIMIT)
        
        try:
            pagination = paginator.page(page)
        except PageNotAnInteger:
            pagination = paginator.page(1)
        except EmptyPage:
            return handleResponseMessage(status.HTTP_200_OK, "No item left.")
        
        serializer = serializers.AnimeSerializer(pagination, many=True)
        return handleResponseMessage(
            status.HTTP_200_OK,
            'Successfully retrieved feed.',
            serializer.data)
    else:
        return handleResponseMessage(status.HTTP_401_UNAUTHORIZED,'Authentication error.')


@api_view(['GET'])
def getAnimeByGenre(request, parameter):
    if request.user.is_authenticated:        
        animeList = models.AnimeModel.objects.filter(
            genres__genre__iregex=parameter
        ).annotate(
            avg_rating=Avg('anime_review__rating')
        )
        
        page = request.GET.get('page')
        paginator = Paginator(animeList, ANIME_PAGINATION_LIMIT)
        
        try:
            pagination = paginator.page(page)
        except PageNotAnInteger:
            pagination = paginator.page(1)
        except EmptyPage:
            return handleResponseMessage(status.HTTP_200_OK, "No item left.")
        
        serializer = serializers.AnimeSerializer(pagination, many=True)
        return handleResponseMessage(
            status.HTTP_200_OK,
            'Successfully retrieved feed.',
            serializer.data)
    else:
        return handleResponseMessage(status.HTTP_401_UNAUTHORIZED,'Authentication error.')
