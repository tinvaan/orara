import json

from django.http import HttpResponse, HttpResponseNotFound

from events.models import OraraEvent
from profiles.utils import events_for
from profiles.models import UserInterests


def summary(request):
    '''
    Summary of upcoming events in proximity
    '''
    try:
        user = UserInterests.objects.get(user=request.user)
        events = events_for(user)
    except UserInterests.DoesNotExist:
        events = OraraEvent.objects.all()

    response = []
    for event in events:
        response.append({
            'name': event.name,
            'description': event.description,
            'venue': {
                'name': event.venue,
                'area': event.venue_area,
                'lat': str(event.venue_lat),
                'lon': str(event.venue_lon)
            },
            'contact': {
                'email': event.email,
                'phone': event.phone,
                'website': event.website,
            },
            'date': str(event.timestamp),
            'tags': list(event.tags.names())
        })
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def invites(request):
    '''
    Events the logged in user has been invited to
    '''
    return HttpResponse("TODO")


def expired(request):
    '''
    Events that expired recently.
    '''
    return HttpResponse("TODO")


def details(request, id):
    '''
    Detailed information about a particular event.
    '''
    return HttpResponse("TODO")


def event_flocks(request, id):
    '''
    People in your circles going to a particular event
    '''
    return HttpResponse("TODO")


def flocks_invited(request, id):
    '''
    People the logged in user has invited to an event.
    '''
    return HttpResponse("TODO")