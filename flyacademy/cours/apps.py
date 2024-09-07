from django.apps import AppConfig


class CoursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cours'

    def ready(self) -> None:
        import cours.signals
