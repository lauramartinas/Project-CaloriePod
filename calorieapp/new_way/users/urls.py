from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [

    path('', views.userlist, name='userlist'),
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('upload', views.upload_view, name='upload'),
    path('profile', views.profile_view, name='profile'),
    path('profile_update', views.profile_update, name='profile_update'),
    path("contact", views.contact, name="contact"),
    

]

