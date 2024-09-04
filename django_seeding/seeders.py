import pandas
import json
from django.db import models
from django.conf import settings
from django.http import HttpRequest
from rest_framework import serializers
from django_seeding.models import AppliedSeeder
from django_seeding.hashable_dict import HashableDict
from django_seeding.cache_methods import replace_item


class Seeder():
    """ 
    The `Seeder` class provides a minimal class which may be used
    for writing custom seeding implementations.
    
    Required:
        seed:
            `seed()` as <method>

    Additionals:
        priority:
            `priority` as <class attribute>
            or
            `get_priority()` as <method>

        just_debug:
            `just_debug` as <class attribute>
            or
            `get_just_debug()` as <method>:
    """
    def seed(self):
        """ Method that fill the datebase as wanted """
        raise NotImplementedError('`seed()` must be implemented.')
    
    def _seed(self, debug: bool = None):
        """ Inner method that do validation before calling the public `seed()` method """

        if debug is None:
            debug = settings.DEBUG

        # if this seeder is just_debug and the settings state is not debug then dont apply it
        if self._get_just_debug() and not debug:
            return
        
        id = self._get_id()

        # if this seeder is applied before then dont apply it
        if AppliedSeeder.objects.filter(id=id).exists():
            return
        
        PURPLE_COLOR = "\033[35m"
        GREEN_COLOR = "\033[32m"
        WHITE_COLOR = "\033[0m"

        print(f'{PURPLE_COLOR}  Seeding {id}...{WHITE_COLOR}', end='')
        
        # apply the seeder 
        self.seed()

        # store it in the applied seeders table in the database
        AppliedSeeder.objects.create(id=id)

        print(F'{GREEN_COLOR}Successfully ^_^{WHITE_COLOR}')

    def get_priority(self):
        """ 
        Method return the `priority` value (smaller will be applied earlier)
        
        if `priority` is passed:
            it will be returned

        if `priority` is not passed:
            float(inf) will be returned 
        """
        return getattr(self, 'priority', float('inf'))
    
    def _get_priority(self):
        """ Inner method to validate the value returned by `get_priority()` method """
        priority = self.get_priority()

        if not isinstance(priority, float) and not isinstance(priority, int):
            raise TypeError('`priority` must be a number')
        
        return priority

    def get_just_debug(self):
        """ 
        Method return the `just_debug` value 
        
        just_debug=True means this seeder will be applied just when settings.DEBUG=True
        
        if `just_debug` is passed:
            it will be returned

        if `just_debug` is not passed:
            False will be returned 
        """
        return getattr(self, 'just_debug', False)
    
    def _get_just_debug(self):
        """ Inner method to validate the value returned by `get_just_debug()` method """
        just_debug = self.get_just_debug()

        if not isinstance(just_debug, bool):
            raise TypeError('`just_debug` must be a bool value')
        
        return just_debug
    
    def get_id(self):
        """ 
        Method return the `id` value to be stored in the database `AppliedSeeder` table

        Note: by this id value we can check if this seeder is applied before or not
        
        it is preferred to not change the id 
        because after changing thd id the seeder will be considerd as another seeder
        then it will be apllied even that the old seeder is applied with the old id value

        default value is the name of the class -> str(type(self))

        Note:
        if you changed the class name 
        or changed the seeder-class file name
        or and file in the path from the root to the class the str(type(self)) will return another value
        then the default value of this seeder is changed
        then if it doesnt have a constant id the seeder will be applied again
        and it may cause errors

        so:
        give an `id` class attribute to solv this problem
        """
        return getattr(self, 'id', str(type(self)))
    
    def _get_id(self):
        """ Inner method to validate the value returned by `get_id()` method """
        id = self.get_id()

        if not isinstance(id, str):
            raise TypeError('`id` must be str')
        
        return id


class DataSeeder(Seeder):
    """
    The `DataSeeder` class provides a minimal class which may be used
    for writing custom seeding implementations.
    
    Required:
        data:
            `data` as <class attribute>
            or
            `get_data()` as <method>
    """
    def get_data(self):
        """ Method return the `data` that will be seeded """
        data = getattr(self, 'data', None)

        if data is None:
            raise TypeError('subclasses of `DataSeeder` must have `data` class attribute or the `get_data()` method')
        
        return data
    
    def _get_data(self):
        """ Inner method to validate the value returned by `get_data()` method """
        data = self.get_data()

        error_message = '`data` must be list of dict'

        if not isinstance(data, list):
            raise TypeError(error_message)
        
        for record_data in data:
            if not isinstance(record_data, dict):
                raise TypeError(error_message)
        
        return data


class ModelSeeder(DataSeeder):
    """
    The `ModelSeeder` class  is a subclasse of `DataSeeder` needs `model` and provides fast `seed()` implementation with `bulk_create()` method.
    
    Required:
        model:
            `model` as <class attribute>
            or
            `get_model()` as <method>
    """
    def get_model(self):
        """ Method return the `model` that will be seeded """
        model = getattr(self, 'model', None)

        if model is None:
            raise TypeError('subclasses of `ModelSeeder` must have `model` class attribute or the `get_model()` method')
        
        return model
    
    def _get_model(self):
        """ Inner method to validate the value returned by `get_model()` method """
        model = self.get_model()

        if not isinstance(model, type) or not issubclass(model, models.Model):
            raise TypeError('`model` must be a subclasse of `django.db.models.Model`')
        
        return model

    def seed(self):
        """ Standard Implementation of `seed()` method with `bulk_create()` """
        data = self._get_data()
        model = self._get_model()
        new_objects = [model(**record_data) for record_data in data]
        model.objects.bulk_create(new_objects)
    

class SerializerSeeder(DataSeeder):
    """
    The `SerializerSeeder` class  is a subclasse of `DataSeeder` needs `serializer_class` and provides slow `seed()` implementation.

    Note: this class is slow not like `ModelSeeder`, so if you have a big dataset dont use this class
    
    Required:
        serializer_class:
            `serializer_class` as <class attribute>
            or
            `get_serializer_class()` as <method>
    """
    def get_serializer_class(self):
        """ Method return the `serializer_class` that will be used in seeding """
        serializer_class = getattr(self, 'serializer_class', None)

        if serializer_class is None:
            raise TypeError('subclasses of SerializerSeeder must have serializer_class class attribute or the get_serializer_class method')
        
        return serializer_class
    
    def _get_serializer_class(self):
        """ Inner method to validate the value returned by `get_serializer_class()` method """
        serializer_class = self.get_serializer_class()

        if not isinstance(serializer_class, type) or not issubclass(serializer_class, serializers.Serializer):
            raise TypeError('serializer_class must be a subclasse of rest_framework.serializers.Serializer')
        
        return serializer_class
    
    def seed(self):
        """ Slow Implementation of `seed()` method with `serializer.save()` method for every record """
        data = self._get_data()
        serializer_class = self._get_serializer_class()
        for record_data in data:
            request = HttpRequest()
            request.user = None
            serializer = serializer_class(data=record_data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        

class EmptySeeder(ModelSeeder):
    """
    The `EmptySeeder` class is a subclasse of `ModelSeeder` needs `records_count` and provides fast `seed()` implementation with `bulk_create()` method.
    
    Required:
        records_count:
            `records_count` as <class attribute>
            or
            `get_records_count()` as <method>
    """
    def get_records_count(self):
        """ Method return the `records_count` that will be used in seeding """
        records_count = getattr(self, 'records_count', None)

        if records_count is None:
            raise TypeError('subclasses of EmptySeeder must have records_count class attribute or the get_records_count method')
        
        return records_count
    
    def _get_records_count(self):
        """ Inner method to validate the value returned by `get_records_count()` method """
        records_count = self.get_records_count()

        if not isinstance(records_count, int):
            raise TypeError('records_count must be int')
        
        return records_count

    def seed(self):
        """ Standard Implementation of `seed()` method for empty objects with `bulk_create()` """
        records_count = self._get_records_count()
        model = self._get_model()
        new_objects = (model() for _ in range(records_count))
        model.objects.bulk_create(new_objects)
    

class CSVFileReader():
    """
    The `CSVFileReader` class needs `csv_file_path` and provides `get_data()` implementation.
    
    Required:
        csv_file_path:
            `csv_file_path` as <class attribute>
            or
            `get_csv_file_path()` as <method>
    """
    def get_csv_file_path(self):
        """ Method return the `csv_file_path` that will be used in `get_date()` method implementation """
        csv_file_path = getattr(self, 'csv_file_path', None)

        if csv_file_path is None:
            raise TypeError('subclasses of `CSVFileReader` must have `csv_file_path` class attribute or the `get_csv_file_path()` method')
        
        return csv_file_path
    
    def _get_csv_file_path(self):
        """ Inner method to validate the value returned by `get_csv_file_path()` method """
        csv_file_path = self.get_csv_file_path()

        if not isinstance(csv_file_path, str):
            raise TypeError('`csv_file_path` must be str')
        
        return csv_file_path
    
    def get_data(self):
        """ Method (using pandas) read the csv_file that is specified by `csv_file_path` and return the `data` that will be seeded """
        data = []
        csv_file_path = self._get_csv_file_path()
        pandas_file = pandas.read_csv(csv_file_path)
        for _, row in pandas_file.iterrows():
            record_data = {}
            for key, value in row.items():
                record_data[key] = value
            data.append(record_data)
        return data
    

class JSONFileReader():
    """
    The `JSONFileReader` class needs `json_file_path` and provides `get_data()` implementation.
    
    Required:
        json_file_path:
            `json_file_path` as <class attribute>
            or
            `get_json_file_path()` as <method>
    """
    def get_json_file_path(self):
        """ Method return the `json_file_path` that will be used in `get_date()` method implementation """
        json_file_path = getattr(self, 'json_file_path', None)

        if json_file_path is None:
            raise TypeError('subclasses of `JSONFileReader` must have `json_file_path` class attribute or the `get_json_file_path()` method')
        
        return json_file_path
    
    def _get_json_file_path(self):
        """ Inner method to validate the value returned by `get_json_file_path()` method """
        json_file_path = self.get_json_file_path()

        if not isinstance(json_file_path, str):
            raise TypeError('`json_file_path` must be str')
        
        return json_file_path
    
    def get_data(self):
        """ Method read the json_file that is specified by `json_file_path` and return the `data` that will be seeded """
        json_file_path = self._get_json_file_path()
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    
    
class CSVFileModelSeeder(CSVFileReader, ModelSeeder):
    """
    The `CSVFileModelSeeder` class is a Fast Full implemented class that needs `csv_file_path`, 'model` and provides `seed()` implementation.
    
    Required:
        csv_file_path:
            `csv_file_path` as <class attribute>
            or
            `get_csv_file_path()` as <method>

        model:
            `model` as <class attribute>
            or
            `get_model()` as <method>
    """
    pass
    
    
class CSVFileSerializerSeeder(CSVFileReader, SerializerSeeder):
    """
    The `CSVFileSerializerSeeder` class is a Slow Full implemented class that needs `csv_file_path`, 'serializer_class` and provides `seed()` implementation.
    
    Required:
        csv_file_path:
            `csv_file_path` as <class attribute>
            or
            `get_csv_file_path()` as <method>

        serializer_class:
            `serializer_class` as <class attribute>
            or
            `get_serializer_class()` as <method>
    """
    pass
    
    
class JSONFileModelSeeder(JSONFileReader, ModelSeeder):
    """
    The `JSONFileModelSeeder` class is a Fast Full implemented class that needs `json_file_path`, 'model` and provides `seed()` implementation.
    
    Required:
        json_file_path:
            `json_file_path` as <class attribute>
            or
            `get_json_file_path()` as <method>

        model:
            `model` as <class attribute>
            or
            `get_model()` as <method>
    """
    pass
    
    
class JSONFileSerializerSeeder(JSONFileReader, SerializerSeeder):
    """
    The `JSONFileSerializerSeeder` class is a Slow Full implemented class that needs `json_file_path`, 'serializer_class` and provides `seed()` implementation.
    
    Required:
        json_file_path:
            `json_file_path` as <class attribute>
            or
            `get_json_file_path()` as <method>

        serializer_class:
            `serializer_class` as <class attribute>
            or
            `get_serializer_class()` as <method>
    """
    pass


class JSONFileChildSeeder(JSONFileModelSeeder):
    """
    The `JSONFileChildSeeder` is a subclass of `JSONFileModelSeeder`.
    Use this class to seed models that are related to other models.
    The model that will be seeded (aka child model) has a `models.ForeignKey` field which references the parent model.
    """
    
    def seed(self):
        """ Implementation of `seed()` method for child models """
        data = self._get_data()
        model = self._get_model()

        data = tuple(HashableDict(record_data) for record_data in data)
        for record_data in data:
            replace_item(model, model, record_data)

        new_objects = [model(**record_data) for record_data in data]
        model.objects.bulk_create(new_objects)
