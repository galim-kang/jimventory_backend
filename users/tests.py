from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserModel(TestCase):
    def test_user_model_creation(self):
        user = CustomUser.objects.create_user(username="test@example.com", email="test@example.com", password="test12345", user_type='tourist')
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.user_type, 'tourist')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

class TestUserAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "test@example.com",
            "email": "test@example.com",
            "password": "test12345",
            "user_type": "tourist"
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_signup(self):
        new_user_data = {
            "username": "newuser@example.com",
            "email": "newuser@example.com",
         "password": "newpassword123",
          "user_type": "tourist"
       }
        response = self.client.post(reverse('signup'), new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)

    def test_user_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-details'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user(self):
        self.client.force_authenticate(user=self.user)
        new_data = {"email": "updated@example.com"}
        response = self.client.put(reverse('user-update'), new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")

    def test_delete_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('user-delete'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(email=self.user.email)
