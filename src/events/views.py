import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound

from flocks.utils import has_connection
from profiles.utils import events_for
from profiles.models import UserInterests
from events.models import OraraEvent, EventInvites, EventCustomers


def complete(request):
    '''
    An exhaustive list of all upcoming events
    '''
    response = []
    for event in OraraEvent.objects.all():
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


@login_required
def explore(request):
    '''
    Summary of upcoming events in proximity,
    catered specifically to a user's interests.
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


@login_required
def invites(request):
    '''
    Events the logged in user has been invited to
    '''
    events = []
    for event in EventInvites.objects.filter(user=request.user):
        events.append({
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
    return HttpResponse(json.dumps(events, indent=4),
                        content_type="application/json")


def expired(request):
    '''
    Events that expired recently.
    '''
    return HttpResponse("TODO")


def details(request, id):
    '''
    Detailed information about a particular event.
    '''
    try:
        event = OraraEvent.objects.get(id=id)
    except OraraEvent.DoesNotExist:
        return HttpResponseNotFound("Requested event not found")

    return HttpResponse(json.dumps({
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
        'tags': list(event.tags.names()),
        'categories': event.categories
    }, indent=4), content_type="application/json")


@login_required
def flocks_subscribed(request, id):
    '''
    People in your circles going to a particular event
    '''
    try:
        event = OraraEvent.objects.get(id=id)
    except OraraEvent.DoesNotExist:
        return HttpResponseNotFound("Requested event not found")

    customers = []
    for item in EventCustomers.objects.filter(event=event):
        if has_connection(request.user, item.customer):
            customers.append({
                'name': item.customer.name(),
                'status': item.customer.status,
                'area': item.customer.area,
                'phone': item.customer.phone,
            })

    customers = {} if len(customers) == 0 else customers
    return HttpResponse(json.dumps(customers, indent=4),
                        content_type="application/json")


@login_required
def flocks_invited(request, id):
    '''
    People the logged in user has invited to an event.
    '''
    try:
        event = OraraEvent.objects.get(id=id)
    except OraraEvent.DoesNotExist:
        return HttpResponseNotFound("Requested event not found")

    users = []
    for invite in OraraEvent.objects.filter(invited_by=request.user, event=event):
        users.append({
            'name': invite.user.name(),
            'status': invite.user.status,
            'area': invite.user.area,
            'phone': invite.user.phone,
        })
    users = {} if len(users) == 0 else users
    return HttpResponse(json.dumps(users, indent=4),
                        content_type="application/json")
