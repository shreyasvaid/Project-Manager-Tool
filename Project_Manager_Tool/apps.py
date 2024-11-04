# apps.py
from django.apps import AppConfig

class HelloConfig(AppConfig):  # Replace 'HelloConfig' with your app’s config class if different
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Project_Manager_Tool'  # Make sure this matches your app name

    def ready(self):
        import Project_Manager_Tool.signals  # Import your signals module here
