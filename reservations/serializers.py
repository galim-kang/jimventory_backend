# reservations/serializers.py

from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Reservation
        fields = '__all__'
