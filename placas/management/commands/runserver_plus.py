import webbrowser
import threading
from django.core.management.commands.runserver import Command as RunserverCommand

class Command(RunserverCommand):
    def inner_run(self, *args, **options):
        threading.Timer(1.5, lambda: webbrowser.open('http://127.0.0.1:8000/camera/')).start()
        return super().inner_run(*args, **options)
