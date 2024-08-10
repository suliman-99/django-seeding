import pandas
import json
from django.db import models
from django.conf import settings
from django.http import HttpRequest
from rest_framework import serializers
from django_seeding.models import AppliedSeeder


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
    The `JSONFileChildSeeder` is a subclass of `JSONFileModelSeeder`, needs `heritage`.
    Use this class to seed models that are related to other models. The model that will be seeded (aka child model) has a `models.ForeignKey` field which references the parent model.
    """
    # def get_heritage(self):
    #     """ Method return the `heritage` of the model that will be seeded """
    #     heritage = getattr(self, 'heritage', None)

    #     if heritage is None:
    #         raise TypeError('subclasses of `JSONFileChildSeeder` must have `parent_models` class attribute or the `get_parent_models()` method')

    #     return heritage
    
    # def _get_heritage(self):
    #     """ Inner method to validate the value returned by `get_heritage()` method """
    #     heritage = self.get_heritage()

    #     if not isinstance(heritage, dict):
    #         raise TypeError('`heritage` must be a dictionary')
        
    #     for key in heritage.keys():
    #         if not issubclass(key, models.Model):
    #             raise TypeError('each `heritage` key must be a subclass of `django.db.models.Model`')
    #     # continue to check heritage properties
    #     return heritage
    
    # def get_parent_models(self):
    #     """ Method return the `parent_models` of the model that will be seeded """
    #     parent_models = getattr(self, 'parent_models', None)

    #     if parent_models is None:
    #         raise TypeError('subclasses of `JSONFileChildSeeder` must have `parent_models` class attribute or the `get_parent_models()` method')
        
    #     return parent_models
    
    # def _get_parent_models(self):
    #     """ Inner method to validate the value returned by `get_parent_models()` method """
    #     parent_models = self.get_parent_models()

    #     if not isinstance(parent_models, list):
    #         raise TypeError('`parent_models` must be list of subclasses of `django.db.models.Model`')
        
    #     for item in parent_models:
    #         if not issubclass(item, models.Model):
    #             raise TypeError('each `parent_models` entry must be a subclasses of `django.db.models.Model`')

    #     return parent_models
    
    # def get_keys_dict(self):
    #     """
    #     Method return the `keys_dict` of {fk: pk}
    #     Where pk is the primary key field name of the parent model and fk is the foreign key field name of the child model that will be seeded """
    #     keys_dict = getattr(self, 'keys_dict', None)

    #     if keys_dict is None:
    #         raise TypeError('subclasses of `JSONFileChildSeeder` must have `keys_dict` class attribute or the `get_keys_dict()` method')

    #     return keys_dict

    # def _get_keys_dict(self):
    #     """ Inner method to validate the value returned by `get_keys_dict()` method """
    #     keys_dict = self.get_keys_dict()
    #     model = self.get_model()
    #     child_model_fields = [field.name for field in model._meta.fields]
    #     parent_models = self.get_parent_models()

    #     if not isinstance(keys_dict, dict):
    #         raise TypeError('`keys_dict` must be a dict')
        
    #     if len(parent_models) != len(keys_dict):
    #         raise IndexError('`keys_dict` and `parent_models` must have the same size')

        # for fk, p_model in zip(keys_dict.keys(), parent_models):
        #     # Check if keys (fk) in keys_dict are fields in child_model
        #     if fk not in child_model_fields:
        #         raise Exception(f'"{fk}" is not a "{model.__name__}" field')
            
        #     # Check if the values (pk) are fields in parent_models
        #     p_model_fields = [field.name for field in p_model._meta.fields]
        #     pk = dict[fk]
        #     if isinstance(pk, list):
        #         for pk_item in pk:
        #             if pk_item not in p_model_fields:
        #                 raise Exception(f'"{pk_item}" is not a "{p_model.__name__}" field')
            
        #     if pk not in p_model_fields:
        #         raise Exception(f'"{pk}" is not a "{p_model.__name__}" field')

        # return keys_dict
    
    def seed(self):
        """ Implementation of `seed()` method for child models """
        model = self._get_model()
        data = self._get_data()
        hashmap = dict()

        def _buscas(tabela, dici, mod_entry):
            if not tabela in hashmap:
                hashmap[tabela] = dict()

            fields_info = { field.verbose_name: field.related_model for field in tabela._meta.fields if field.is_relation }

            for item, subitens in dici.items():
                if item in fields_info:
                    mod_entry[item] = _buscas(fields_info[item], subitens, mod_entry[item])
                elif isinstance(subitens, str):
                    try:
                        if subitens in hashmap[tabela]:
                            pk_obj = hashmap[tabela][subitens]

                        else:
                            pk_obj = tabela.objects.get(**{item: subitens})
                            hashmap[tabela][subitens] = pk_obj
                    except tabela.DoesNotExist:
                        # TO-DO: create parent instance?
                        # ... parent_model.objects.create()
                        
                        raise Exception(f'Error: instance of "{tabela.__name__}": "{subitens}" does not exist! Please change your seeder.json and try again...')
                    else:
                        return pk_obj                

        for entry in data:
            _buscas(model, {k : v for k, v in entry.items() if isinstance(v, dict)}, entry)

            # for related_model, keys_dict in heritage.items():
            #     for rm_field in keys_dict.i

            # for fk_name, p_model in zip(keys_dict.keys(), parent_models):
            #     pk_name = keys_dict[fk_name]
            #     # print(f'pk: {pk_name}, fk: {fk_name}')
            
            #     fk = entry.get(fk_name)

            #     try:
            #         pk_obj = p_model.objects.get(**{pk_name: fk})
            #         # print(pk_obj)
            #     except p_model.DoesNotExist:
            #         # TO-DO: create parent instance?
            #         # ... parent_model.objects.create()
                    
            #         raise Exception(f'Error: instance of "{p_model.__name__}": "{pk_name}" = "{fk}" does not exist! Please change your seeder.json and try again...')
            #     else:
            #         entry[fk_name] = pk_obj

        new_objects = [model(**entry) for entry in data]
        model.objects.bulk_create(new_objects)
