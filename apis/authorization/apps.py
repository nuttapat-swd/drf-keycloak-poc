from django.apps import AppConfig


class AuthorizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apis.authorization'

    def ready(self):
        import apis.authorization.receiver