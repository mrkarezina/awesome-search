from django.urls import path

from .views import general_search

urlpatterns = [
    path(r'', general_search, name="general-search")
]
