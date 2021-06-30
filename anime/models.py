from django.db import models
from django.conf import settings
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']

class AnimeModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    studio = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    premierSeason = models.CharField(max_length=255)
    episodes = models.IntegerField()
    about = models.CharField(max_length=1250)
    images = ImageSerializer(many=True, required=False)
    trailer = models.URLField(max_length = 255)
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.user.name) + ' reported ' + str(self.feed.id)
    
class AnimeReviewModel(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.CharField(max_length=550)