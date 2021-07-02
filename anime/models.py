from django.db import models
from django.conf import settings
from manga.models import MangaModel
import uuid
from common.models import CharacterModel, Genres

def upload_location(instance, filename, **kwargs):
    file_path = 'anime/{uuid}/{filename}'.format(
            uuid=uuid.uuid4(),
            filename=filename
		) 
    return file_path


class AnimeGenreModel(models.Model):
    genre = models.CharField(max_length=255, choices=Genres.choices, default=Genres.Action)
    
    def __str__(self):
        return str(self.genre)    


class AnimeModel(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=upload_location)
    name = models.CharField(max_length=255)
    studio = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    genres = models.ManyToManyField(AnimeGenreModel)
    characters = models.ManyToManyField(CharacterModel, blank=True)
    premierSeason = models.CharField(max_length=255)
    episodes = models.IntegerField()
    about = models.TextField()
    trailer = models.URLField(max_length=255)
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.name)


class RelationOrderModel(models.Model):
    order = models.IntegerField()
    anime = models.ForeignKey(AnimeModel, on_delete=models.CASCADE, related_name="anime_relation", blank=True, null=True)

    def __str__(self):
        return str(self.order) + ' ' + str(self.anime.name)

class RelationModel(models.Model):
    adaptation = models.ForeignKey(MangaModel, on_delete=models.DO_NOTHING, related_name="adaptation", blank=True, null=True)
    series = models.ManyToManyField(RelationOrderModel, blank=True)


class AnimeReviewModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.TextField()
    date = models.DateTimeField(auto_now=True, verbose_name="anime review date")
    rating = models.IntegerField()
    anime = models.ForeignKey(AnimeModel, on_delete=models.CASCADE, related_name="anime_review", blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'anime'], name='reviewAnimeConstraint')
        ]

    def __str__(self):
        return str(self.user.username) + ' gave score ' + str(self.rating) + ' to ' + str(self.anime.name)


class Image(models.Model):
    image = models.ImageField(upload_to=upload_location)
    anime = models.ForeignKey(AnimeModel, on_delete=models.CASCADE, related_name="anime_images")
    
    def __str__(self):
        return self.image.name