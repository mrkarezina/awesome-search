from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TweetsViewSet

router = DefaultRouter()
router.register(r'tweets', TweetsViewSet)

# URLs determined automatically by the router
# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#binding-viewsets-to-urls-explicitly
urlpatterns = [
    path('', include(router.urls)),
]

# import pprint
# pprint.pprint(router.get_urls())

