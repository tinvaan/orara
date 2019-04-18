from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from profiles.models import OraraUser
from profiles.contexts import profile_info, social_info
from profiles.utils import interested_events, registered_events
from flocks.utils import invites, has_connection, suggestions, connections


def signin(request):
    user = authenticate(username=request.POST.get('user_name'),
                        password=request.POST.get('user_pass'))
    if user is not None:
        login(request, user)
        return home(request)
    return render(request, 'profiles/login.html')


@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    return render(request, 'home.html', {
        'profile': profile_info(request.user),
        'social': social_info(request.user),
        'invites': invites(request.user),
        'connections': connections(request.user),
        'suggested': {
            'flocks': suggestions(request.user),
            'events': []
        }
    })


@login_required
def profile(request, username):
    try:
        user = OraraUser.objects.get(username=username)
    except OraraUser.DoesNotExist:
        return HttpResponseNotFound("Profile info for '{}' not found"\
                                    .format(username))

    context = {
        'profile': profile_info(request.user),
        'social': social_info(user),
        'user': {
            'username': username,
            'name': user.name(),
            'first_name': user.first_name,
            'status': user.status,
            'bio': user.bio,
            'area': user.area,
            'college': user.college,
            'workplace': user.workplace,
            'photo': user.photo
        },
        'events': {
            'interested': interested_events(user),
            'registered': registered_events(user)
        },
        'owner': request.user == user,
        'connection': has_connection(request.user, user)
    }
    return render(request, 'profiles/profile.html', context)
