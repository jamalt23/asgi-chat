import asyncio, json
from asgiref.sync import sync_to_async
from django.http import HttpRequest, StreamingHttpResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from core.models import Message

@login_required
async def delete_message(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        try:
            # Check if the message exists and belongs to the user
            await Message.objects.filter(id=int(message_id), author=request.user).adelete()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

async def stream_chat_messages(request: HttpRequest) -> StreamingHttpResponse:
    """
    Streams chat messages to the client as they are created or deleted.
    """
    async def event_stream():
        """
        Send a continuous stream of data to the connected clients.
        """
        previous_messages = await get_all_message_ids()

        while True:
            current_messages = await get_all_message_ids()

            new_messages: list[Message] = await sync_to_async(list)(
                Message.objects.filter(
                    id__in=current_messages.difference(previous_messages))
            )

            if new_messages:
                for message in new_messages:
                    message = await sync_to_async(message.dict)()
                    yield f"data: {json.dumps({'action': 'create', 'message': message})}\n\n"

            deleted_messages = previous_messages.difference(current_messages)
            if deleted_messages:
                for message_id in deleted_messages:
                    yield f"data: {json.dumps({'action': 'delete', 'message_id': message_id})}\n\n"

            previous_messages = current_messages
            await asyncio.sleep(0.1)  # To reduce db queries

    async def get_all_message_ids() -> set[int]:
        messages = await sync_to_async(list)(
            Message.objects.all().values_list('id', flat=True)
        )
        return set(messages)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

