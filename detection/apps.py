from django.apps import AppConfig
import threading

class DetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detection'

    def ready(self):
        from detection.services.capture_service import start_camera_detection

        thread = threading.Thread(target=start_camera_detection)
        thread.daemon = True
        thread.start()
