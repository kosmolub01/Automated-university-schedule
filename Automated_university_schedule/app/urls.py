from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # All URLs below start with '/app/'.
    path('', views.index, name='index'),
    path('view_schedule/', views.view_schedule, name='view_schedule'),
    path('change_group/', views.change_group, name='change_group'),
    path('update_schedules/', views.login_page, name='login_page'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('update_the_schedules/', views.update_the_schedules, name='update_the_schedules'),
    path('check_scraper_progress/', views.check_scraper_progress, name='check_scraper_progress'),
]