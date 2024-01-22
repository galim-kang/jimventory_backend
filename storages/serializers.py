# storage/serializers.py
from rest_framework import serializers
from .models import Storage, Menu

class StorageSerializer(serializers.ModelSerializer):
    hostUser = serializers.ReadOnlyField(source='hostUser.username')

    class Meta:
        model = Storage
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
