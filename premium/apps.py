from django.apps import AppConfig


class PremiumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'premium'

    def ready(self):
        import premium.models
