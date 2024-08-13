from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPassword.as_view(), name='password-reset'),
    path('reset-password/<uidb64>/<token>/', ResetPassword.as_view(), name='password-reset-confirm'),
]