
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Tweet


class TweetCreateTests(APITestCase):

    def test_create_tweet(self):
        url = reverse('tweet-list')
        tweet = {
            'tweet_id': 1345884177842003970,
            'body': "To help quickly find in-depth articles from engineering blogs, @maskys_ and I put together a Google Programmable Search for the 650 blogs listed here https://github.com/kilimchoi/engineering-blogs. Search: https://bit.ly/eng-blogs",
            'author_screen_name': 'mrkarezina'
        }
        response = self.client.post(url, tweet, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tweet['id'] = 1
        self.assertDictEqual(response.data, tweet)


class TweetOperationsTests(APITestCase):

    def setUp(self):
        Tweet.objects.create(
            tweet_id=1345884177842003970,
            body="To help quickly find in-depth articles from engineering blogs, @maskys_ and I put together a Google Programmable Search for the 650 blogs listed here https://github.com/kilimchoi/engineering-blogs. Search: https://bit.ly/eng-blogs",
            author_screen_name='mrkarezina'
        )

    def test_list_tweets(self):
        url = reverse('tweet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(response.data[0], {
            'id': 1,
            'tweet_id': 1345884177842003970,
            'body': "To help quickly find in-depth articles from engineering blogs, @maskys_ and I put together a Google Programmable Search for the 650 blogs listed here https://github.com/kilimchoi/engineering-blogs. Search: https://bit.ly/eng-blogs",
            'author_screen_name': 'mrkarezina'
        })
