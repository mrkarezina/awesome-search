from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    # path('search/', include('apps.decks.urls')),
    # path('cards/', include('apps.cards.urls')),
]
