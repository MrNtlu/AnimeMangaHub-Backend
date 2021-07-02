from rest_framework import serializers
from common import models

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterModel
        fields  = ['name','about','image']