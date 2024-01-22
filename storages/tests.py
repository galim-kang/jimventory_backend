from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Storage

User = get_user_model()

class StorageAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.storage = Storage.objects.create(
            hostUser=self.user,
            storeType='Type1',
            serviceName='Test Storage',
            address='Test Address',
            latitude=37.7749,
            longitude=-122.4194,
            operatingTime={"open": "10:00", "close": "22:00"},
            description={"description": "Test Description"},
            introduction='Test Introduction',
            available=True,
            contact_info='123456789'
        )

    def test_create_storage(self):
        data = {
            'hostUser': self.user.id,
            'storeType': 'Type2',
            'serviceName': 'New Test Storage',
            'address': 'New Address',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'operatingTime': {"open": "09:00", "close": "21:00"},
            'description': {"description": "New Description"},
            'introduction': 'New Introduction',
            'available': True,
            'contact_info': '987654321'
        }
        response = self.client.post(reverse('storage-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_storage_list(self):
        response = self.client.get(reverse('storage-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_storage(self):
        data = {
            'serviceName': 'Updated Test Storage',
            'available': False
        }
        response = self.client.put(reverse('storage-update', args=[self.storage.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.storage.refresh_from_db()
        self.assertEqual(self.storage.serviceName, 'Updated Test Storage')
        self.assertEqual(self.storage.available, False)

    def test_storage_detail(self):
        """
        특정 저장소 상세 정보 조회 테스트
        """
        response = self.client.get(reverse('storage-detail', args=[self.storage.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_storage_delete(self):
        """
        저장소 삭제 테스트
        """
        response = self.client.delete(reverse('storage-detail', args=[self.storage.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


### 코드 설명
# - **setUp 메소드**: 테스트 실행 전 필요한 사용자와 저장소 인스턴스를 설정합니다.
# - **test_create_storage**: 새로운 저장소를 생성하고, HTTP 201 상태 코드를 확인합니다.
# - **test_storage_list**: 저장소 목록을 조회하고, HTTP 200 상태 코드를 확인합니다.
# - **test_update_storage**: 특정 저장소의 정보를 업데이트하고, HTTP 200 상태 코드와 업데이트된 데이터를 확인합니다.
# - **test_storage_detail**: 특정 저장소의 상세 정보를 조회하고, HTTP 200 상태 코드를 확인합니다.
# - **test_storage_delete**: 특정 저장소를 삭제하고, HTTP 204 상태 코드를 확인합니다.
