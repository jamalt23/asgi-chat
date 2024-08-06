from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.urls import reverse_lazy
from accounts.forms import LoginForm, SignUpForm

def signup(request: HttpRequest):
    next_page = request.GET.get('next')
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            if next_page:
                return redirect(next_page)
            return redirect('core:home')
    return render(request, 'signup.html', {'form': form})

class Login(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:home') 

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)
