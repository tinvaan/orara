from django.urls import path

from . import views


app_name = 'profiles'
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.signin, name='signin'),
    path('logout', views.signout, name='signout')
]
