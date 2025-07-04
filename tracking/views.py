import asyncio
from django.http import StreamingHttpResponse
from channels.layers import get_channel_layer
import json

async def location_stream(request):
    """
    An asynchronous view that streams location updates via SSE.
    """
    channel_layer = get_channel_layer()
    
    # Each web client connects to a unique channel
    # We'll use a group to broadcast to all of them
    group_name = "location_updates"
    async def event_stream():
        # Create a unique channel for this specific client connection
        channel_name = await channel_layer.new_channel()
        await channel_layer.group_add(group_name, channel_name)
        
        try:
            while True:
                # Listen for a message on the unique channel
                message = await channel_layer.receive(channel_name)
                
                # When a message is received, format it as an SSE event and yield it
                data = message['data']
                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(0.1) # Prevent tight looping
        finally:
            # Clean up when the client disconnects
            await channel_layer.group_discard(group_name, channel_name)
    
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    # The 'X-Accel-Buffering' header is important for Nginx to prevent it from buffering the response.
    response['X-Accel-Buffering'] = 'no'
    return response