from django.apps import AppConfig
from django.conf import settings


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from mongoengine import connect
        from mongoengine.connection import _connections, _connection_settings
        print(_connections, _connection_settings)
        connect(**settings.MONGO_DATABASES)
        print(_connections, _connection_settings)
