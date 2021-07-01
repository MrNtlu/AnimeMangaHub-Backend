from django.contrib import admin
from anime import models

admin.site.register(models.AnimeModel)
admin.site.register(models.AnimeGenreModel)
admin.site.register(models.RelationModel)
admin.site.register(models.RelationOrderModel)
admin.site.register(models.AnimeReviewModel)
admin.site.register(models.Image)