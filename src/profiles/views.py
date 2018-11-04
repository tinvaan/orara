from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from profiles.models import OraraUser
from profiles.utils import interested_events, registered_events


def signin(request):
    user = authenticate(username=request.POST.get('user_name'),
                        password=request.POST.get('user_pass'))
    if user is  not None:
        login(request, user)
        return home(request)
    return render(request, 'profiles/login.html')


@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    return render(request, 'base.html')


@login_required
def profile(request, username):
    if request.user.username == username:
        try:
            user = OraraUser.objects.get(username=username)
        except OraraUser.DoesNotExist:
            return HttpResponseNotFound("Profile info for '{}' not found"\
                                        .format(username))

        context = {
            'user': {
                'username': username,
                'name': user.name(),
                'first_name': user.first_name,
                'status': user.status,
                'area': user.area,
                'phone': user.phone,
                'email': user.email,
                'photo': user.photo
            },
            'events': {
                'interested': interested_events(user),
                'registered': registered_events(user)
            }
        }
        return render(request, 'profiles/profile.html', context)
    else:
        return HttpResponseNotFound("Profile infor for '{}' not found"\
                                    .format(username))
