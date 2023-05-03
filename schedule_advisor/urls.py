from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'schedule_advisor'
urlpatterns = [
    path('', views.index, name='index'),
    path('browse/', views.browse, name='browse'),
    path('schedule/', views.schedule, name='schedule'),
    path('advisor/', views.advisor, name='advisor'),
    path('accounts/login', views.login, name = 'login'),
    path('accounts/signup', views.signup, name = 'signup')
]