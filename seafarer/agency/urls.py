from django.urls import path

from . import views

app_name = 'agency'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('crew/add', views.crew_add, name='crew_add'),
    path('crew/manage', views.crew_manage, name='crew_manage'),
    path('crew/manage/<int:pk>/', views.crew_manage_one, name='crew_manage_one'),
    path('crew/manage/<int:pk>/edit', views.crew_edit, name='crew_edit'),
    path('crew/manage/<int:pk>/delete', views.crew_delete, name='crew_delete'),
    path('charters/add', views.charters_add, name='charters_add'),
    path('ships', views.ships, name='ships'),
    path('analytics', views.analytics, name='analytics'),
    path('apply', views.apply, name='apply'),
    path('test', views.test, name='test'),
]