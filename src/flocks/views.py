import json

from django.http import HttpResponse, HttpResponseNotFound

from flocks.utils import match_percentage
from profiles.models import OraraUser, SocialProfiles, UserInterests


def summary(request):
    '''Fetch all users in proximity, sorted by
    - Age range
    - Gender
    - Common places(school, work, band, NGO, etc)
    - Mutual friends
    - Languages spoken
    - Common cities
    '''
    return HttpResponse("TODO")


def profile(request, id):
    '''
    Profile information of a particular user in flocks
    '''
    return HttpResponse("TODO")


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