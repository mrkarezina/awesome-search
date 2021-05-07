from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class UserLoginTests(APITestCase):

    def setUp(self):
        self.test_user = {
            'username': 'admin',
            'password': 'password123',
            'email': 'admin@admin.com'
        }
        self.client = APIClient()
        user = User.objects.create_user(self.test_user['username'],
                                        self.test_user['email'],
                                        self.test_user['password'])
        self.token = AuthToken.objects.create(user)

    def test_login_user(self):
        url = reverse('login')
        response = self.client.post(url, data={
            'username': self.test_user['username'],
            'password': self.test_user['password'],
        })
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['user']['id'], 1)
        self.assertEqual(data['user']['username'], self.test_user['username'])
        self.assertIsNotNone(data['token'])

    def test_deny_register_existing_user(self):
        url = reverse('register')
        response = self.client.post(url, data={
            'username': self.test_user['username'],
            'password': self.test_user['password'],
            'email': self.test_user['password'],
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user(self):
        url = reverse('register')
        response = self.client.post(url, data={
            'username': 'admin2',
            'password': 'pass2',
            'email': 'admin2@admin.com',
        })
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data['token'])
        self.assertEqual(data['user']['username'], 'admin2')
