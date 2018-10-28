from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = "flocks"
urlpatterns = [
    path('', views.summary, name='summary'),
    path('explore', views.explore, name='explore'),
    path('stumbled', views.stumbled, name='stumbled'),
    path('bookmarks', views.bookmarks, name='bookmarks'),
    path('users/<str:name>', views.profile, name='profile'),
    path('connections', views.connections, name='connections')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
