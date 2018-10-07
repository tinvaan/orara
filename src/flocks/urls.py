from django.urls import path

from . import views


app_name = "flocks"
urlpatterns = [
    path('', views.all, name='all'),
    path('stumbled', views.stumbled, name='stumbled'),
    path('bookmarks', views.bookmarks, name='bookmarks')
]