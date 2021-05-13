from django.db.models import query
from django.http import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .formatter import format_query, parse


class GeneralSearchTests(APITestCase):

    def test_query_formatter(self):
        query = format_query('redis search', resources=['tweets', 'github'],
                             languages=['Python', 'Ruby'], awesome_lists=['awesome-python', 'awesome-ruby'])
        target = "@source:(tweets|github) @language:(Python|Ruby) @lists:(awesome-python awesome-ruby) redis search"
        self.assertEquals(query, target)

    def test_query_parser(self):
        query = "redis-*search"
        query = parse(query)
        self.assertEqual(query, "redis*search")

    def test_general_search(self):
        url = reverse("general-search")
        response = self.client.get(url, {'query': 'awesome'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['docs'])

    def test_faceted_search(self):
        url = reverse("general-search")
        response = self.client.get(url, {'query': 'python', 'source': [
                                   'tweets', 'github'], 'language': ['Python', 'Ruby']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['docs'])

    def test_language_list(self):
        url = reverse("search-languages")
        response = self.client.get(url)
        self.assertIsNotNone(response.json()['languages'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_awesome_list_list(self):
        url = reverse("search-lists")
        response = self.client.get(url)
        self.assertIsNotNone(response.json()['lists'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
