from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User  # Assurez-vous d'importer votre modèle User

class UserAPITest(TestCase):
    def test_setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_all_users(self):
        url = reverse('user-list')  # Assurez-vous que 'user-list' correspond à votre nom d'URL pour la liste des utilisateurs
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').exists(), True)

    def test_update_user(self):
        user_id = self.user.id
        url = reverse('user-detail', kwargs={'pk': user_id})
        data = {'username': 'updateduser'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=user_id).username, 'updateduser')

    def test_delete_user(self):
        user_id = self.user.id
        url = reverse('user-detail', kwargs={'pk': user_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(id=user_id).exists(), False)
