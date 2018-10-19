from django.urls import path

from . import views


app_name = "flocks"
urlpatterns = [
    path('', views.summary, name='summary'),
    # path('<str:username>', views.profile, name='profile'),
    path('explore', views.explore, name='explore'),
    path('stumbled', views.stumbled, name='stumbled'),
    path('bookmarks', views.bookmarks, name='bookmarks'),
]