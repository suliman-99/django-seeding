from django.core.management.commands.runserver import Command as BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from ...seeder_registry import SeederRegistry
        SeederRegistry.import_all_then_seed_all()
