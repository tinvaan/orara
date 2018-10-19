import json

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from flocks.utils import match_percentage
from profiles.models import OraraUser, SocialProfiles, UserInterests


def summary(request):
    return HttpResponseRedirect('/flocks/explore')


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



def stumbled(request):
    '''
    Fetch all users you've connected with in previous events.
    '''
    return HttpResponse("TODO")


def bookmarks(request):
    '''
    Fetch all users you've shown an interest in.
    '''
    return HttpResponse("TODO")