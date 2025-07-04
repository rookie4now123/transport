from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import LocationPoint

@receiver(post_save, sender=LocationPoint)
def broadcast_location(sender, instance, created, **kwargs):
    """
    When a new LocationPoint is saved, broadcast it to the group.
    """
    if created:
        channel_layer = get_channel_layer()
        # Serialize the instance data
        # Note: You might want a simpler serializer for the broadcast
        data = {
            "route_id": str(instance.run.route.id),
            "route_name": instance.run.route.route_name,
            "monitor_name": instance.run.monitor.username,
            "run_id": str(instance.run.id),
            "latitude": float(instance.location.y),
            "longitude": float(instance.location.x),
            "timestamp": instance.timestamp.isoformat()
        }
        
        # Use async_to_sync to call the async group_send method from sync code
        async_to_sync(channel_layer.group_send)(
            "location_updates",  # The name of the group to send to
            {
                "type": "send_location", # This is a custom event type, the name doesn't matter much for this simple SSE
                "data": data,
            }
        )