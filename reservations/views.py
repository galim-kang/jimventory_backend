# reservations/views.py
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Reservation
from .serializers import ReservationSerializer
from .permissions import IsOwnerOrAdmin

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'host':  # 'is_host' 대신 'user_type'을 사용
            return Reservation.objects.filter(storage__hostUser=user)
        return Reservation.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ModifyReservationView(views.APIView):
    permission_classes = [IsOwnerOrAdmin]

    def put(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CancelReservationView(views.APIView):
    permission_classes = [IsOwnerOrAdmin]

    def delete(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        reservation.status = 'cancelled'  # Soft delete: changing status to cancelled
        reservation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
