import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound,\
                        HttpResponseRedirect

from events.models import EventCustomers
from profiles.models import OraraUser, UserInterests
from profiles.contexts import profile_info, social_info
from flocks.models import UserBookmarks, OraraConnections
from flocks.utils import nearby, segregate, match_percentage, get_customers


@login_required
def summary(request):
    '''
    Complete list of users in database
    '''
    users = []
    context = {}
    for user in OraraUser.objects.all():
        if not user == request.user:
            users.append({
                'username': user.username,
                'name': user.name(),
                'bio': user.bio,
                'area': user.area,
                'status': user.status,
                'college': user.college,
                'workplace': user.workplace,
                'photo': user.photo
            })
    friends, others = segregate(request.user, users)
    context = {
        'profile': profile_info(request.user),
        'social': social_info(request.user),
        'found': True,
        'users': others,
        'connections': friends
    }
    return render(request, 'flocks/summary.html', context)


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
        'username': user.username,
        'name': user.name(),
        'bio': user.bio,
        'status': user.status,
        'area': user.area,
        'college': user.college,
        'workplace': user.workplace,
        'photo': user.photo
    }, indent=4), content_type="application/json")


@login_required
def explore(request):
    '''
    Find people with similar interests around you
    (consider: age, gender, common places, mutual friends, langauges, etc)
    '''
    users = nearby(request.user)
    friends, others = segregate(request.user, users)
    context = {
        'profile': profile_info(request.user),
        'social': social_info(request.user),
        'users': others,
        'connections': friends,
        'found': len(users) > 0
    }
    return render(request, 'flocks/summary.html', context)


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
            'username': bookmark.bookmark.username,
            'name': bookmark.bookmark.name(),
            'area': bookmark.bookmark.area,
            'status': bookmark.bookmark.status,
            'college': bookmark.bookmark.college,
            'workplace': bookmark.bookmark.workplace
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
            'username': connection.user2.username,
            'name': connection.user2.name(),
            'area': connection.user2.area,
            'status': connection.user2.status,
            'college': connection.user2.college,
            'workplace': connection.user2.workplace
        })
    for connection in OraraConnections.objects.filter(user2=request.user, approved=True):
        response.append({
            'username': connection.user1.username,
            'name': connection.user1.name(),
            'area': connection.user1.area,
            'status': connection.user1.status,
            'college': connection.user1.college,
            'workplace': connection.user1.workplace
        })

    response = {} if len(response) == 0 else response
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")