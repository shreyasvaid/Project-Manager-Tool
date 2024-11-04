from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/<str:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<str:project_id>/delete/', views.delete_project, name='delete_project'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/<str:task_id>/edit/', views.edit_task, name='edit_task'),  # Changed to <str:task_id>
    path('tasks/<str:task_id>/delete/', views.delete_task, name='delete_task'),  # Changed to <str:task_id>
    path('modify_project/', views.modify_project, name='modify_project'),
    path('modify_task/', views.modify_task, name='modify_task'),
    path('project_report/', views.project_report, name='project_report'),
    path('team_members/add/', views.add_team_member, name='add_team_member'),
    path('team_members/<str:member_id>/edit/', views.edit_team_member, name='edit_team_member'),
    path('team_members/<str:member_id>/delete/', views.delete_team_member, name='delete_team_member'),
    path('team_members/modify/', views.modify_team_member, name='modify_team_member'),  # Add this line if missing
]
