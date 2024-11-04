# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Project, Task, TeamMember

def generate_id(prefix, count):
    """Helper function to generate an ID with a prefix and zero-padded count."""
    return f"{prefix}{str(count + 1).zfill(3)}"  # e.g., PROJ001, TASK001

@receiver(pre_save, sender=Project)
def set_project_id(sender, instance, **kwargs):
    if not instance.project_id:  # Only set ID if it's not already set
        last_project = Project.objects.order_by('-project_id').first()
        if last_project and last_project.project_id.startswith("PROJ"):
            last_id = int(last_project.project_id[4:])
            instance.project_id = generate_id("PROJ", last_id)
        else:
            instance.project_id = "PROJ001"

@receiver(pre_save, sender=Task)
def set_task_id(sender, instance, **kwargs):
    if not instance.task_id:  # Only set ID if it's not already set
        last_task = Task.objects.order_by('-task_id').first()
        if last_task and last_task.task_id.startswith("TASK"):
            last_id = int(last_task.task_id[4:])
            instance.task_id = generate_id("TASK", last_id)
        else:
            instance.task_id = "TASK001"

@receiver(pre_save, sender=TeamMember)
def set_team_member_id(sender, instance, **kwargs):
    if not instance.member_id:  # Only set ID if it's not already set
        last_member = TeamMember.objects.order_by('-member_id').first()
        last_id = int(last_member.member_id[2:]) if last_member and last_member.member_id.startswith("TM") else 0
        instance.member_id = generate_id("TM", last_id)