from rest_framework import serializers
from .models import RadioShow

class RadioShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioShow
        fields = '__all__'
