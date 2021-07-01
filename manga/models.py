from django.db import models

class MangaModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    volumes = models.IntegerField()
    chapters = models.IntegerField()
    published = models.CharField(max_length=255)
    #genres = models.CharField(max_length=255)
    about = models.TextField()
    
    def __str__(self):
        return str(self.id) + ' ' + str(self.name)