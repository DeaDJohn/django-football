from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path( '', views.index, name = "index" ),
    path('update_teams/', views.update_teams, name='update_teams'),
    path('update_countries/', views.update_countries, name='update_countries'),
    
]