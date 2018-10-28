from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'base.html')


def signin(request):
    user = authenticate(username=request.POST.get('user_name'),
                        password=request.POST.get('user_pass'))
    if user is  not None:
        login(request, user)
        return home(request)
    return render(request, 'profiles/login.html')


def signout(request):
    logout(request)
    return HttpResponseRedirect('/')
