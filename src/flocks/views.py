import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound,\
                        HttpResponseRedirect

from events.models import EventCustomers
from profiles.models import OraraUser, UserInterests
from flocks.utils import match_percentage, get_customers
from flocks.models import UserBookmarks, OraraConnections


@login_required
def summary(request):
    return HttpResponseRedirect('/flocks/explore')


@login_required
def profile(request, name):
    '''
    Profile information of a particular user in flocks
    '''
    try:
        user = OraraUser.objects.get(username=name)
    except OraraUser.DoesNotExist:
        return HttpResponseNotFound("User '{}' not found".format(name))
    return HttpResponse(json.dumps({
        'name': user.name(),
        'status': user.status,
        'area': user.area,
        'phone': user.phone
    }, indent=4), content_type="application/json")


@login_required
def explore(request):
    '''
    Find people with similar interests around you
    (consider: age, gender, common places, mutual friends, langauges, etc)
    '''
    users = []

    # No filters are applicable if user hasn't registered any interests
    try:
        UserInterests.objects.get(user=request.user)
    except UserInterests.DoesNotExist:
        for user in OraraUser.objects.all():
            users.append({
                'name': user.name(),
                'area': user.area,
                'status': user.status,
                'phone': user.phone
            })
        return HttpResponse(json.dumps(users, indent=4),
                            content_type="application/json")

    # Filter by
    # 1) Location | TODO: Narrow down using lat/lon in next iteration
    # 2) Interests
    for user in OraraUser.objects.filter(area=request.user.area):
        try:
            interest = UserInterests.objects.get(user=user)
            if not match_percentage(interest.user, request.user) == 0:
                users.append({
                    'name': user.name(),
                    'area': user.area,
                    'status': user.status,
                    'phone': user.phone
                })
        except UserInterests.DoesNotExist:
            pass

    users = users if len(users) else {}
    return HttpResponse(json.dumps(users, indent=4),
                        content_type="application/json")


@login_required
def stumbled(request):
    '''
    Fetch all users you've connected with in previous events.
    '''
    customers = []
    for item in EventCustomers.objects.filter(customer=request.user):
        customers.append(get_customers(item.event))
    customers = {} if len(customers) == 0 else customers
    return HttpResponse(json.dumps(customers, indent=4),
                        content_type="application/json")


@login_required
def bookmarks(request):
    '''
    Fetch all users you've shown an interest in.
    '''
    response = []
    for bookmark in UserBookmarks.objects.all():
        response.append({
            'name': bookmark.bookmark.name(),
            'area': bookmark.bookmark.area,
            'status': bookmark.bookmark.status,
            'phone': bookmark.bookmark.phone
        })

    response = {} if len(response) == 0 else response
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


@login_required
def connections(request):
    '''
    Return all connections for a user
    '''
    response = []
    for connection in OraraConnections.objects.filter(user1=request.user, approved=True):
        response.append({
            'name': connection.user2.name(),
            'area': connection.user2.area,
            'status': connection.user2.status,
            'phone': connection.user2.phone
        })
    for connection in OraraConnections.objects.filter(user2=request.user, approved=True):
        response.append({
            'name': connection.user1.name(),
            'area': connection.user2.area,
            'status': connection.user2.status,
            'phone': connection.user2.phone
        })

    response = {} if len(response) == 0 else response
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")