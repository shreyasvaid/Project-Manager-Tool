from django.db import models

class TeamMember(models.Model):
    member_id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    project_id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100, db_index=True) # index
    description = models.TextField()
    start_date = models.DateField() 
    end_date = models.DateField() 

    def __str__(self):
        return self.name

class Task(models.Model):
    task_id = models.CharField(primary_key=True, max_length=100)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', db_index=True) # index
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, related_name='tasks')

    def __str__(self):
        return self.title
