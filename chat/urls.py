from django.urls import path
from . import views

urlpatterns = [
    path('friends', views.users, name='users'),
    path('chat/<int:thread>/',views.chat,name='chat'),
    path('thekonera',views.send ,name='send'),
    path("getmessages/<str:thread>",views.getmessages,name='getmessages'),
    path('search/' , views.search_address),


]