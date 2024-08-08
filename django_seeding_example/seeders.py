from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry 
from django_seeding_example.models import *
from django_seeding_example.serializers import *


@SeederRegistry.register
class M1Seeder(seeders.CSVFileModelSeeder):
    id = 'M1Seeder'
    priority = 1
    model = M1
    csv_file_path = 'django_seeding_example/seeders_data/M1Seeder.csv'


@SeederRegistry.register
class M2Seeder(seeders.JSONFileModelSeeder):
    id = 'M2Seeder'
    priority = 2
    model = M2
    json_file_path = 'django_seeding_example/seeders_data/M2Seeder.json'


@SeederRegistry.register
class M3Seeder(seeders.CSVFileSerializerSeeder):
    id = 'M3Seeder'
    priority = 3
    serializer_class = M3Serializer
    csv_file_path = 'django_seeding_example/seeders_data/M3Seeder.csv'


@SeederRegistry.register
class M4Seeder(seeders.JSONFileSerializerSeeder):
    id = 'M4Seeder'
    priority = 4
    serializer_class = M4Serializer
    json_file_path = 'django_seeding_example/seeders_data/M4Seeder.json'


@SeederRegistry.register
class M5Seeder(seeders.EmptySeeder):
    id = 'M5Seeder'
    priority = 5
    model = M5
    records_count = 2


@SeederRegistry.register
class M6Seeder(seeders.ModelSeeder):
    id = 'M6Seeder'
    priority = 6
    model = M6
    data = [
        {
            "title": "in-code t1",
            "description": "in-code d1"
        },
        {
            "title": "in-code t2",
            "description": "in-code d2"
        },
    ]


@SeederRegistry.register
class M7Seeder(seeders.SerializerSeeder):
    id = 'M7Seeder'
    priority = 7
    serializer_class = M7Serializer
    data = [
        {
            "title": "in-code t1",
            "description": "in-code d1"
        },
        {
            "title": "in-code t2",
            "description": "in-code d2"
        },
    ]


@SeederRegistry.register
class CustomSeeder(seeders.Seeder):
    id = 'CustomSeeder'
    priority = 8
    
    def seed(self):
        post1 = Post.objects.create(content='post1')
        post2 = Post.objects.create(content='post1')

        comment1 = Comment.objects.create(post=post1, content='comment1')
        comment2 = Comment.objects.create(post=post1, content='comment2')
        comment3 = Comment.objects.create(post=post2, content='comment3')
        comment4 = Comment.objects.create(post=post2, content='comment4')


@SeederRegistry.register
class Parent1Seeder(seeders.JSONFileModelSeeder):
    id = 'Parent1Seeder'
    priority = 9
    model = Parent1
    json_file_path = 'django_seeding_example/seeders_data/Parent1Seeder.json'


@SeederRegistry.register
class Child1Seeder(seeders.JSONFileChildModelSeeder):
    id = 'Child1Seeder'
    model = Child1
    parent_model = Parent1
    keys_dict = {'name': 'parent'}
    json_file_path = 'django_seeding_example/seeders_data/Child1Seeder.json'
