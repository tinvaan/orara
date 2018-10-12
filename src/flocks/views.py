from django.shortcuts import render
from django.http import HttpResponse


def summary(request):
    '''Fetch all users in proximity, sorted by
    - Age range
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