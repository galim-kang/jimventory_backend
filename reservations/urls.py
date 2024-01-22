# reservations/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, ModifyReservationView, CancelReservationView

router = DefaultRouter()
router.register(r'', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
    path('modify/<int:pk>/', ModifyReservationView.as_view(), name='modify-reservation'),
    path('cancel/<int:pk>/', CancelReservationView.as_view(), name='cancel-reservation'),

]
