from django.urls import path

from levelupreports.views.users.eventsbygamer import UserEventList
from .views import UserGameList

urlpatterns = [
    path('reports/usergames', UserGameList.as_view()),
    path('reports/userevents', UserEventList.as_view())
]