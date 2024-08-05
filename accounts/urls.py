from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    # path('logout/', logout, name='logout'),
]