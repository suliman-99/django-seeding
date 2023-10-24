from django.apps import AppConfig


class DjangoSeedingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_seeding'

    def ready(self):
        from .seeder_registry import SeederRegistry
        SeederRegistry.on_run()
        return super().ready()
