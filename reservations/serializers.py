from rest_framework import serializers
from .models import Reservation
from storages.models import Storage

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['hostUser', 'storeType', 'serviceName', 'address', 'latitude', 'longitude', 'operatingTime', 'description', 'introduction', 'available', 'image', 'contact_info']

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    storage = StorageSerializer()  # Storage에 대한 정보를 포함

    class Meta:
        model = Reservation
        fields = '__all__'
