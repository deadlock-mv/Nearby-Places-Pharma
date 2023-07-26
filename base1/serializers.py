from rest_framework import serializers
from base1.models import StoreMaster, StoreCompetition

class StoreCompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = StoreCompetition