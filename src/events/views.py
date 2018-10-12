from django.http import HttpResponse


def summary(request):
    '''
    Summary of upcoming events in proximity
    '''
    return HttpResponse("TODO")


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