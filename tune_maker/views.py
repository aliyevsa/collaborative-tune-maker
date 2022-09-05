from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from .models import *

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
    else:
        user_form = UserForm()

    return render(request, 'tune_maker/register.html', { 'user_form': user_form, 'registered': registered })

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/projects/')
    else:
        login_form = LoginForm()

    return render(request, 'tune_maker/login.html', { 'login_form': login_form })

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def index(request):    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project()
            project.name = form.cleaned_data['name']
            project.length = form.cleaned_data['length']
            owner_pk = request.user.id
            project.owner = User.objects.get(pk=owner_pk)
            project.collaborator = form.cleaned_data['collaborator']
            project.save()
            return HttpResponseRedirect('/')
    else:
        form = ProjectForm()

    return render(request, 'tune_maker/index.html', { 'form': form })

@login_required
def projects(request):
    owner_pk = request.user.id
    owned_projects = Project.objects.filter(owner=owner_pk)
    collaborated_projects = Project.objects.filter(collaborator=owner_pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project()
            project.name = form.cleaned_data['name']
            project.length = form.cleaned_data['length']
            project.owner = User.objects.get(pk=owner_pk)
            project.collaborator = form.cleaned_data['collaborator']
            project.save()
            
            for i in range(form.cleaned_data['length']):
                notes = Notes()
                notes.save()
                tune_row = TuneRow()
                tune_row.project = project
                tune_row.number = i
                tune_row.notes = notes
                tune_row.save()
            
            return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm()
    
    return render(request, 'tune_maker/projects.html', { 'owned_projects': owned_projects, 'collaborated_projects': collaborated_projects, 'form': form })

@login_required
def project(request, project_id):
    owner_pk = request.user.id
    project = Project.objects.get(pk=project_id)
    project_accessible = False

    if project.collaborator:
        project_accessible = project.owner.id == owner_pk or project.collaborator.id == owner_pk
    else:
        project_accessible = project.owner.id == owner_pk

    if project_accessible:
        tune_rows = TuneRow.objects.filter(project=project)
        tune_rows_notes = []
        for tune_row in tune_rows:
            tune_rows_notes.append(tune_row.notes.get_notes())

        return render(request, 'tune_maker/project.html', { 'project': project, 'project_id': project_id, 'tune_rows': tune_rows_notes })
    else:
        return render(request, 'tune_maker/projects.html')

def public_project(request, project_id):
    return render(request, 'tune_maker/public_project.html', { 'project_id': project_id })

@login_required
def discussion(request, project_id):
    owner_pk = request.user.id
    project = Project.objects.get(pk=project_id)
    project_accessible = False

    if project.collaborator:
        project_accessible = project.owner.id == owner_pk or project.collaborator.id == owner_pk
    else:
        project_accessible = project.owner.id == owner_pk

    if project_accessible:
        return render(request, 'tune_maker/discussion.html', { 'project': project, 'project_id': project_id })
    else:
        return render(request, 'tune_maker/projects.html')
