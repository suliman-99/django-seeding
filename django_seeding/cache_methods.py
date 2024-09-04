from functools import lru_cache
from django.db import models


@lru_cache(maxsize=None)
def get_object(model: models.Model, record_data: dict):
    return model.objects.get(**record_data)


@lru_cache(maxsize=None)
def replace_item(initial_model: models.Model, model: models.Model, record_data: dict):
    """ replace item in the record_data with the db object """

    related_keys_dict = {
        field.name: field.related_model 
        for field in model._meta.fields 
        if field.is_relation
    }

    for k, v in record_data.items():
        if k in related_keys_dict:
            if isinstance(v, dict):
                record_data[k] = replace_item(initial_model, related_keys_dict[k], v)

    if model == initial_model:
        return
    
    return get_object(model, record_data)
