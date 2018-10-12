from django.urls import path

from . import views


app_name = 'events'
urlpatterns = [
    path('', views.summary, name='summary'),
    path('invites', views.invites, name='invites'),
    path('expired', views.expired, name='expired'),
    path('<int:id>', views.details, name='details'),
    path('<int:id>/flocks', views.event_flocks, name='event_flocks'),
    path('<int:id>/flocks/invited', views.flocks_invited, name='flocks_invited'),
]