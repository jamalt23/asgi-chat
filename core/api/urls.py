from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('delete-message/', delete_message, name='delete-message'),
    path('stream-chat-messages/', stream_chat_messages, name='stream-chat-messages'),
]
