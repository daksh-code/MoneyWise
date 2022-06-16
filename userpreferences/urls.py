from django.contrib import admin
from django.urls import path,include
from .views import UserProfile
from . import views
urlpatterns = [
     path('',views.UserProfile,name='userprofile'),
]