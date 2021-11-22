from django.db.models.manager import BaseManager
from django.urls import path
from .import views

urlpatterns = [ 
    path('' ,  views.home  , name="home"),
    path('logout', views.logout_view, name='logout'),
    path('<int:ano>', views.post, name='post'),
    path('feedback', views.feedback_view, name='feedback'),
]