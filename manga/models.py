from django.db import models
from common.models import CharacterModel, Genres
from django.conf import settings


class MangaGenreModel(models.Model):
    genre = models.CharField(max_length=255, choices=Genres.choices, default=Genres.Action)
    
    def __str__(self):
        return str(self.genre)


class MangaModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    volumes = models.IntegerField()
    chapters = models.IntegerField()
    published = models.CharField(max_length=255)
    characters = models.ManyToManyField(CharacterModel, blank=True)
    genres = models.ManyToManyField(MangaGenreModel)
    about = models.TextField()
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.name)
    
class MangaReviewModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.TextField()
    date = models.DateTimeField(auto_now=True, verbose_name="manga review date")
    rating = models.IntegerField()
    manga = models.ForeignKey(MangaModel, on_delete=models.CASCADE, related_name="manga_review", blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'manga'], name='reviewMangaConstraint')
        ]

    def __str__(self):
        return str(self.user.username) + ' gave score ' + str(self.rating) + ' to ' + str(self.manga.name)
