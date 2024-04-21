from django.core.management.commands.runserver import Command as BaseCommand
from django_seeding.seeder_registry import SeederRegistry
from django_seeding.casting_methods import cast_to_bool


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--debug', type=str, help='Debug Mode')
        super().add_arguments(parser)

    def handle(self, *args, **options):
        SeederRegistry.import_all_then_seed_all(debug=cast_to_bool(options.get('debug')))
