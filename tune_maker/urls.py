from django.contrib.auth.decorators import login_required
from django.urls import path
from . import api
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', login_required(login_url='/login/')(views.user_logout), name='logout'),
    path('projects/', login_required(login_url='/login/')(views.projects), name='projects'),
    path('project/<int:project_id>/', login_required(login_url='/login/')(views.project), name='project'),
    path('public/project/<int:project_id>/', views.public_project, name='public_project'),
    path('discussion/<int:project_id>/', login_required(login_url='/login/')(views.discussion), name='discussion'),
    path('api/tune_rows/<int:project_id>/', api.TuneRowsAPI.as_view(), name='tune_rows_api'),
    path('api/notes/<int:pk>/', api.NotesAPI.as_view(), name='notes_api'),
    # path('api/project/<int:pk>/', api.ProjectAPI.as_view(), name='project_api'),
]
