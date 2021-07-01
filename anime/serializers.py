from rest_framework import serializers
from anime import models

class GenreSerializer(serializers.ModelSerializer):
    genre = serializers.ChoiceField(choices=models.AnimeGenreModel.Genres)
    
    class Meta:
        model = models.AnimeGenreModel
        fields = ['genre']
        

class AnimeSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = models.AnimeModel
        fields  = ['id','name','studio','type','genres','characters','premierSeason',
                  'episodes','about','trailer','rating']
        
    def get_rating(self, obj):
        if obj.avg_rating == None:
            return 0.0
        return obj.avg_rating