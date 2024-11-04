from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task, TeamMember
from .forms import ProjectForm, TaskForm, TeamMemberForm
from django.db import connection

# Homepage
def index(request):
    return render(request, 'index.html')

# Project views
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})

def edit_project(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})

def delete_project(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('index')
    return render(request, 'confirm_delete.html', {'object': project, 'type': 'Project'})

# Task views
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print("Form errors:", form.errors)  # Debug: print form errors to console
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})

def delete_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    return render(request, 'confirm_delete.html', {'object': task, 'type': 'Task'})

# Report view
def project_report(request):
    # Get the project ID from the request (if provided)
    selected_project_id = request.GET.get('project_id')
    
    # Fetch all projects to populate the dropdown menu
    all_projects = Project.objects.all()

    report_data = []
    if selected_project_id:
        # Retrieve data for the selected project
        query_projects = '''
            SELECT project_id, name, description, start_date, end_date
            FROM hello_project
            WHERE project_id = %s
        '''
        with connection.cursor() as cursor:
            cursor.execute(query_projects, [selected_project_id])
            projects = cursor.fetchall()

        for project in projects:
            project_id, name, description, start_date, end_date = project

            # Query to get task status counts for the selected project
            query_tasks = '''
                SELECT status, COUNT(*) AS total
                FROM hello_task
                WHERE project_id = %s
                GROUP BY status
            '''
            with connection.cursor() as cursor:
                cursor.execute(query_tasks, [project_id])
                task_counts = cursor.fetchall()

            # Query to get all tasks with assigned team members for the selected project
            query_task_details = '''
                SELECT t.title, t.description, t.status, t.due_date, m.name AS assigned_to
                FROM hello_task t
                LEFT JOIN hello_teammember m ON t.assigned_to_id = m.member_id
                WHERE t.project_id = %s
            '''
            with connection.cursor() as cursor:
                cursor.execute(query_task_details, [project_id])
                tasks = cursor.fetchall()

            # Organize tasks and status counts for this project
            task_statuses = [{'status': row[0], 'total': row[1]} for row in task_counts]
            task_details = [
                {'title': row[0], 'description': row[1], 'status': row[2], 'due_date': row[3], 'assigned_to': row[4]}
                for row in tasks
            ]

            # Append all data for this project to the report
            report_data.append({
                'project_id': project_id,
                'name': name,
                'description': description,
                'start_date': start_date,
                'end_date': end_date,
                'task_statuses': task_statuses,
                'tasks': task_details,
            })

    return render(request, 'project_report.html', {
        'report_data': report_data,
        'all_projects': all_projects,
        'selected_project_id': selected_project_id
    })

# Modify views for projects and tasks
def modify_project(request):
    projects = Project.objects.all()
    return render(request, 'modify_project.html', {'projects': projects})

def modify_task(request):
    tasks = Task.objects.all()
    return render(request, 'modify_task.html', {'tasks': tasks})

def add_team_member(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TeamMemberForm()
    return render(request, 'add_team_member.html', {'form': form})

def edit_team_member(request, member_id):
    team_member = get_object_or_404(TeamMember, member_id=member_id)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, instance=team_member)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TeamMemberForm(instance=team_member)
    return render(request, 'edit_team_member.html', {'form': form})

def delete_team_member(request, member_id):
    team_member = get_object_or_404(TeamMember, member_id=member_id)
    if request.method == 'POST':
        team_member.delete()
        return redirect('index')
    return render(request, 'confirm_delete.html', {'object': team_member, 'type': 'Team Member'})

def modify_team_member(request):
    team_members = TeamMember.objects.all()
    return render(request, 'modify_team_member.html', {'team_members': team_members})
