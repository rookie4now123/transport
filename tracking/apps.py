from django.apps import AppConfig


class TrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracking'
    label = 'tracking'
    def ready(self):
        """
        This method is called when the app is ready.
        We import our signals module here to connect the signals.
        """
        import tracking.signals  # This line is the only thing you need to add.