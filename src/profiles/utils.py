from profiles.models import UserInterests
from events.models import OraraEvent, EventLikes, EventCustomers


def suggested_events(user):
    try:
        instance = UserInterests.objects.get(user=user)
    except UserInterests.DoesNotExist:
        return OraraEvent.objects.all()

    events = []
    for event in OraraEvent.objects.all():
        if instance.interests in event.categories:
            events.append(event)
    return events


def interested_events(user):
    def tags(names):
        result = []
        for name in names:
            result.append(name)
        return result

    likes = []
    for like in EventLikes.objects.filter(user=user):
        likes.append({
            'name': like.event.name,
            'image': like.event.image,
            'description': like.event.description,
            'venue': {
                'name': like.event.venue,
                'area': like.event.venue_area,
                'lat': like.event.venue_lat,
                'lon': like.event.venue_lon
            },
            'contact': {
                'email': like.event.email,
                'phone': like.event.phone,
                'website': like.event.website,
            },
            'date': like.event.timestamp,
            'tags': tags(like.event.tags.names())
        })
    return likes


def registered_events(user):
    def tags(names):
        result = []
        for name in names:
            result.append(name)
        return result

    registers = []
    for register in EventCustomers.objects.filter(customer=user):
        registers.append({
            'name': register.event.name,
            'image': register.event.image,
            'description': register.event.description,
            'venue': {
                'name': register.event.venue,
                'area': register.event.venue_area,
                'lat': register.event.venue_lat,
                'lon': register.event.venue_lon
            },
            'contact': {
                'email': register.event.email,
                'phone': register.event.phone,
                'website': register.event.website,
            },
            'date': register.event.timestamp,
            'tags': tags(register.event.tags.names())
        })
    return registers
