from django.http import HttpRequest, StreamingHttpResponse, HttpResponse, JsonResponse
from rest_framework.views import APIView
from core.models import *

from django.views.decorators.http import require_POST

import asyncio, json
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user
 
@require_POST
def delete_message(request: HttpRequest) -> HttpResponse:
    message_id = request.POST.get('message_id')
    try:
        # Check if the message exists and belongs to the user
        Message.objects.filter(id=int(message_id), author=request.user).delete()
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)

async def stream_chat_events(request: HttpRequest) -> StreamingHttpResponse:
    """
    Streams chat messages to the client as they are created or deleted.
    """
    user: User = await sync_to_async(get_user)(request)
    
    async def event_stream():
        """
        Send a continuous stream of data to the connected clients.
        """
        try:
            previous_messages = await get_all_message_ids()
            previous_typing_users = await get_typing_users()
            
            # Send initial state
            if previous_typing_users:
                yield f"data: {json.dumps({'action': 'typing', 'users': list(previous_typing_users)})}\n\n"

            while True:
                current_messages = await get_all_message_ids()
                
                # Handle typing users
                typing_users = await get_typing_users()
                if typing_users != previous_typing_users:
                    previous_typing_users = typing_users
                    typing_users = list(typing_users)
                    yield f"data: {json.dumps({'action': 'typing', 'users': typing_users})}\n\n"
                
                # Handle new messages
                new_message_ids = current_messages - previous_messages
                new_messages = await sync_to_async(list)(Message.objects.filter(id__in=new_message_ids))
                for message in new_messages:
                    message = await sync_to_async(message.dict)()
                    yield f"data: {json.dumps({'action': 'create', 'message': message})}\n\n"

                # Handle deleted messages
                deleted_message_ids = previous_messages - current_messages
                for message_id in deleted_message_ids:
                    yield f"data: {json.dumps({'action': 'delete', 'message_id': message_id})}\n\n"

                previous_messages = current_messages
                await asyncio.sleep(0.1)  # To reduce db queries

        except asyncio.CancelledError:
            user.is_typing = False # Reset typing status when the client disconnects
            await user.asave()
            raise asyncio.CancelledError

    async def get_all_message_ids() -> set[int]:
        messages = await sync_to_async(list)(
            Message.objects.all().values_list('id', flat=True)
        )
        return set(messages)

    async def get_typing_users() -> set[str]:
        users = await sync_to_async(list)(
            User.objects.filter(is_typing=True).values_list('username', flat=True)
        )
        return set(users)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

