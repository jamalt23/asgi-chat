import asyncio, json
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import FriendRequest, User

@login_required
def accept_friend_request(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        from_user_username = request.POST.get('from_user')
        try:
            from_user = User.objects.get(username=from_user_username)
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user)
            friend_request.accept()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)
    return HttpResponse(status=400)

@login_required
def reject_friend_request(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        from_user_username = request.POST.get('from_user')
        try:
            from_user = User.objects.get(username=from_user_username)
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user)
            friend_request.reject()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)
    return HttpResponse(status=400)

@login_required
def unfriend(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        friend_username = request.POST.get('friend')
        try:
            friend = User.objects.get(username=friend_username)
            request.user.remove_friend(friend)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)
    return HttpResponse(status=400)

@login_required
def set_typing_status(request: HttpRequest) -> HttpResponse:
    user = request.user
    if request.method == 'POST' and user.is_authenticated:
        is_typing = request.POST.get('is_typing')
        if is_typing == 'true':
            request.user.is_typing = True
        else:
            request.user.is_typing = False
        request.user.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)