# serializers.py

from rest_framework import serializers
from ..models import  WatchList
from ..serializers.company import CompanySerializer

class WatchListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = WatchList
        fields = '__all__'


