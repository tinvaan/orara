from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'profiles'
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.signin, name='signin'),
    path('logout', views.signout, name='signout'),
    path('profiles/<str:username>', views.profile, name='profile'),
    path('profiles/<str:username>/edit', views.profile, name='edit')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
