from django.urls import path

from . import views


app_name = 'events'
urlpatterns = [
    path('', views.complete, name='complete'),
    path('explore', views.explore, name='explore'),
    path('invites', views.invites, name='invites'),
    path('expired', views.expired, name='expired'),
    path('<int:id>', views.details, name='details'),
    path('<int:id>/flocks', views.flocks_subscribed, name='flocks_subscribed'),
    path('<int:id>/flocks/invited', views.flocks_invited, name='flocks_invited'),
]
