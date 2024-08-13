from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from accounts.forms import LoginForm, SignUpForm, PasswordResetForm, SetPasswordForm

class RedirectIfAuthenticated:
    """
    Redirect to the home page if the user is authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

class SignUp(RedirectIfAuthenticated, CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        self.object = form.save()
        auth_login(self.request, self.object) # Login the user
        return redirect(self.get_success_url())

class Login(RedirectIfAuthenticated, LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('core:home') 


class ForgotPassword(RedirectIfAuthenticated, PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'forgot-password.html'
    email_template_name = 'password-reset-email.html'
    success_url = reverse_lazy('accounts:login')

class ResetPassword(RedirectIfAuthenticated, PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'reset-password.html'
    success_url = reverse_lazy('accounts:login')


# class ProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'profile.html'