from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from storages.models import Storage
from .models import Reservation
import uuid

User = get_user_model()

class ReservationAppTests(TestCase):
    def setUp(self):
        unique_suffix = uuid.uuid4().hex  # 고유한 접미사 생성
        self.user = User.objects.create_user(
        username=f'user_{unique_suffix}',
        email=f'user_{unique_suffix}@example.com',
        password='password'
    )
        self.host_user = User.objects.create_user(
        username=f'host_{unique_suffix}',
        email=f'host_{unique_suffix}@example.com',
        password='password'
    )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.storage = Storage.objects.create(
            hostUser=self.host_user,
            storeType='Type1',
            serviceName='Host Storage',
            address='Host Address',
            latitude=37.7749,
            longitude=-122.4194,
            operatingTime={"open": "09:00", "close": "21:00"},
            description={"description": "Storage Description"},
            introduction='Storage Introduction',
            available=True,
            contact_info='987654321'
        )

        self.reservation = Reservation.objects.create(
            user=self.user,
            storage=self.storage,
            check_in='2022-01-01T10:00:00Z',
            check_out='2022-01-02T10:00:00Z',
            bag_count=2,
            notes='Test Notes',
            status='pending'
        )

    def test_create_reservation(self):
        data = {
            'storage': self.storage.id,
            'check_in': '2022-01-03T10:00:00Z',
            'check_out': '2022-01-04T10:00:00Z',
            'bag_count': 3,
            'notes': 'New Reservation',
            'status': 'pending'
        }
        response = self.client.post(reverse('reservation-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reservation_list(self):
        response = self.client.get(reverse('reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_reservation(self):
        data = {
        'storage': self.storage.id,  # 필수 필드 추가
        'notes': 'Updated Notes'
    }
        response = self.client.put(reverse('reservation-detail', args=[self.reservation.id]), data, format='json')
        print(response.data)  # 응답 내용 출력
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_reservation_detail(self):
        response = self.client.get(reverse('reservation-detail', args=[self.reservation.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_delete(self):
        response = self.client.delete(reverse('reservation-detail', args=[self.reservation.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
