from src.base_response import handleResponseMessage
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view
from anime import serializers, models
from django.db.models import Avg
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from rest_framework.pagination import PageNumberPagination
from auth_user.auth import TokenAuthGet


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


@api_view(['GET'])
def getAnime(request, parameter):
    if request.user.is_authenticated:        
        try:
            anime = models.AnimeModel.objects.annotate(
                avg_rating=Avg('anime_review__rating')
            ).get(id=parameter)
        except:
            return handleResponseMessage(status.HTTP_404_NOT_FOUND, "Couldn't find the corresponding Anime.")
        
        # reviews = models.AnimeReviewModel.objects.filter(anime=anime)
        # images = models.Image.objects.filter(anime=anime)
        relation = models.RelationModel.objects.filter(series__anime=anime)
        
        serializer = serializers.AnimeDetailSerializer(anime, context={ 'relation': relation })
        return handleResponseMessage(
            status.HTTP_200_OK,
            'Successfully retrieved anime.',
            serializer.data)
    else:
        return handleResponseMessage(status.HTTP_401_UNAUTHORIZED,'Authentication error.')
    

class PaginationModel(PageNumberPagination):
    page_size = ANIME_PAGINATION_LIMIT
    page_size_query_param = 'page_size'


class AnimeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AnimeSerializer
    queryset = models.AnimeModel.objects.annotate(
        avg_rating=Avg('anime_review__rating')
    )
    authentication_classes = (TokenAuthGet,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    paginator = PaginationModel()