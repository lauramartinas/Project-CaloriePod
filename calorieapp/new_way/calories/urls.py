from django.urls import path

from .views import CalProfile, CalProfilePageView, calprofile

app_name = 'calories'

urlpatterns = [

    path('',CalProfilePageView, name='home'),
    path('calprofile', CalProfile.as_view() , name='calprofile'),

]