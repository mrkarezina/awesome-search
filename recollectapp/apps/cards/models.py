from django.db import models


class Card(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tweet(Card):
    tweet_id = models.BigIntegerField(blank=False)
    body = models.TextField(max_length=280, blank=False)
    author_screen_name = models.CharField(max_length=15, blank=False)

