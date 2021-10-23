from django.urls import path

from . import views

app_name = 'agency'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('crew', views.crew, name='crew'),
    path('charters', views.charters, name='charters'),
    path('ships', views.ships, name='ships'),
    path('analytics', views.analytics, name='analytics'),
    path('apply', views.apply, name='apply'),
    path('test', views.test, name='test'),
]