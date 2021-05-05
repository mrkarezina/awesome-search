from django.http import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class GeneralSearchTests(APITestCase):
    def test_general_search(self):
        url = reverse("general-search")
        response = self.client.get(url, {'query': 'machine learning'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

