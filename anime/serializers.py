from rest_framework import serializers
from anime import models
from common.models import Genres
from common.serializers import CharacterSerializer

class GenreSerializer(serializers.ModelSerializer):
    genre = serializers.ChoiceField(choices=Genres)
    
    class Meta:
        model = models.AnimeGenreModel
        fields = ['genre']
        

class AnimeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    rating = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True)
    characters = CharacterSerializer(models.CharacterModel.objects.all(), many=True, required=False)
    
    class Meta:
        model = models.AnimeModel
        fields  = ['id','name', 'image','studio','type','genres','characters','premierSeason',
                  'episodes','about','trailer','rating']
        
    def get_rating(self, obj):
        if obj.avg_rating == None:
            return 0.0
        return obj.avg_rating


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']


class AnimeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnimeReviewModel
        fields  = ['id','review','date','rating']


class AnimePreviewSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    genres = GenreSerializer(many=True)
    class Meta:
        model = models.AnimeModel
        fields  = ['id','name','image','studio','type','genres',
                   'premierSeason','episodes','about']


class RelationOrderSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField()
    anime = AnimePreviewSerializer()
    class Meta:
        model = models.RelationOrderModel
        fields  = ['order','anime']


class RelationSerializer(serializers.ModelSerializer):
    series = RelationOrderSerializer(many=True)
    class Meta:
        model = models.RelationModel
        fields  = ['series']


class AnimeDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    rating = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True)
    characters = CharacterSerializer(models.CharacterModel.objects.all(), many=True)
    anime_review = AnimeReviewSerializer(models.AnimeReviewModel.objects.all(), many=True)
    anime_images = ImageSerializer(many=True)
    anime_relation = serializers.SerializerMethodField()
    
    class Meta:
        model = models.AnimeModel
        fields  = ['id','name','image','studio','type','genres','characters','premierSeason',
                  'episodes','about','trailer','rating','anime_review','anime_images','anime_relation',]
        
    def get_rating(self, obj):
        if obj.avg_rating == None:
            return 0.0
        return obj.avg_rating
    
    def get_anime_relation(self, obj):
        relation = self.context['relation']
        return RelationSerializer(relation, many=True).data