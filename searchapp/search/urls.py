from django.urls import path

from .views import general_search, languages, awesome_lists

urlpatterns = [
    path('', general_search, name="general-search"),
    path('languages', languages, name="search-languages"),
    path('awesome-lists', awesome_lists, name="search-lists")
]
