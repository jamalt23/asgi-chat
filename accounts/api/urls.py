from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('accept-friend-request/', accept_friend_request, name='accept-friend-request'),
    path('reject-friend-request/', reject_friend_request, name='reject-friend-request'),
    path('unfriend/', unfriend, name='unfriend'),
    path('set-typing-status/', set_typing_status, name='set-typing-status'),
]
