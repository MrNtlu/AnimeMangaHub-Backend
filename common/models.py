from django.db import models
import uuid

def upload_location(instance, filename, **kwargs):
    file_path = 'character/{uuid}/{filename}'.format(
            uuid=uuid.uuid4(),
            filename=filename
		) 
    return file_path

class CharacterModel(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField()
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    
    def __str__(self):
        return str(self.name)
    
class Genres(models.TextChoices):
        Action = "Action"
        Adventure = "Adventure"
        Comedy = "Comedy"
        Drama = "Drama"
        Fantasy = "Fantasy"
        Historical = "Historical"
        Horror = "Horror"
        Magic = "Magic"
        Mecha = "Mecha"
        Music = "Music"
        Mystery = "Mystery"
        Romance = "Romance"
        School = "School"
        SciFi = "Sci-Fi"
        Seinen = "Seinen"
        Shoujo = "Shoujo"
        Shounen = "Shounen"
        SliceofLife = "Slice of Life"
        Sports = "Sports"
        Supernatural = "Supernatural"
