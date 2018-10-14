from events.models import OraraEvent
from profiles.models import UserInterests


def events_for(user):
    try:
        instance = UserInterests.objects.get(user=user)
    except UserInterests.DoesNotExist:
        return OraraEvent.objects.all()

    events = []
    for event in OraraEvent.objects.all():
        if instance.interests in event.categories:
            events.append(event)
    
    return events