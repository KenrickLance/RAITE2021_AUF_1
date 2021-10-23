from django.urls import path

from . import views

app_name = 'agency'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('crew/add', views.crew_add, name='crew_add'),
    path('charters/add', views.charters_add, name='charters_add'),
    path('ships/add', views.ships_add, name='ships_add'),
    path('analytics', views.analytics, name='analytics'),
    path('apply', views.apply, name='apply'),
    path('test', views.test, name='test'),
]