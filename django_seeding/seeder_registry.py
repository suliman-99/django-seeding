import sys
import importlib.util
from pathlib import Path
from django.apps import apps
from django.conf import settings
from .seeders import Seeder
from .models import AppliedSeeder
    

class SeederRegistry:
    """
    The `SeederRegistry` class apply registered seeders when the server is run.

    seeder registering is doing by:
        @SeederRegistry.register as <decorator>
        or
        SeederRegistry.register(<seeder-class>) as <method>
    """
    seeders = []

    @classmethod
    def register(cls, seeder):
        """ Method and decorator to register the seeder-class in the seeders list to be seeded when the server is run """
        if not issubclass(seeder, Seeder):
            raise TypeError('Only subclasses of Seeder class can be registered with SeederRegistry.register')
        cls.seeders.append(seeder())

    @classmethod
    def import_all(cls):
        """ Method that import all `seeders.py` files in the installed apps to register them in the `SeederRegistry` class """
        for app_config in apps.get_app_configs():
            app_name = app_config.name
            module_name = 'seeders'
            file_name = module_name + '.py'
            file_path = Path(app_config.path) / file_name
            if file_path.exists():
                spec = importlib.util.spec_from_file_location(f"{app_name}.{module_name}", str(file_path))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

    @classmethod
    def seed_all(cls):
        """ 
        Method that call seed methods for all registered seeders
        
        sort the seeders depending on the `priority` (less is applied earlier)
        """

        if AppliedSeeder.objects.filter(id__in=[seeder._get_id() for seeder in cls.seeders]).count() != len(cls.seeders):
            BLUE_COLOR = "\033[94m"
            WHITE_COLOR = "\033[0m"
            print(BLUE_COLOR + "Running Seeders: " + WHITE_COLOR)

        cls.seeders.sort(key=lambda seeder: seeder._get_priority())
        for seeder in cls.seeders:
            seeder._seed()

    @classmethod
    def import_all_then_seed_all(cls):
        """
        Note: the decorator `@SeederRegistry.register` will be applied when the file is imported

        so, if the seeder class is written in another file (not in `seeders.py`)
        then it will not be imported
        then it will not be applied when the server is run

        so, to solve this problem you can import any file contains seeder inside the `AppConfig` class of your app
        """

        # import all `seeders.py` files from all installed apps
        cls.import_all()

        # call the `seed_all()` method to apply all the registered seeders
        cls.seed_all()

    @classmethod
    def on_run(cls):
        if 'runserver' not in sys.argv:
            return
        
        try:
            seed = bool(settings.SEEDING_ON_RUNSERVER)
        except AttributeError:
            seed = False
            
        if '--seed' in sys.argv:
            seed = True
        
        if '--dont-seed' in sys.argv:
            seed = False

        if seed:
            cls.import_all_then_seed_all()
