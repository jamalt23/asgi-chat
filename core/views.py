from typing import Any
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import *
from core.models import *

@login_required
def chat(request: HttpRequest):
    messages = Message.objects.all()
    user: User = request.user
    user.is_typing = False
    user.save()

    if request.method == 'POST':
        text = request.POST.get('text')
        if not text.isspace():
            created_message = Message.objects.create(text=text, author=user)
            return JsonResponse({'id': created_message.id})
        return HttpResponse(status=400)

    context = {
        'messages': messages, 'friends': user.friends.all(),
        'friend_requests': user.friend_requests_received.all(),
    }
    return render(request, 'chat.html', context)
