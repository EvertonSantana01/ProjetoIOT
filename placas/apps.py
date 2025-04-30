from django.apps import AppConfig

class PlacasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'placas'

    def ready(self):
        # Remova ou comente esta linha abaixo
        # from detection.services.capture_service import start_camera_detection
        pass
