from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # /app/
    path('', views.index, name='index'),
    path('view_schedule/', views.view_schedule, name='view_schedule'),
    path('change_group/', views.change_group, name='change_group'),
]