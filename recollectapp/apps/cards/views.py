from .models import Tweet
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import TweetSerializer


class TweetsViewSet(ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
