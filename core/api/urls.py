from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('delete-message/', delete_message, name='delete-message'),
    path('stream-chat-events/', stream_chat_events, name='stream-chat-events'),
]
