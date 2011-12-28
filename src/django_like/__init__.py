from django.db import connection
from django.db.models.fields import Field, subclassing
from django.db.models.sql.constants import QUERY_TERMS


QUERY_TERMS['like'] = None
QUERY_TERMS['ilike'] = None
connection.operators['like'] = connection.operators['contains']
connection.operators['ilike'] = connection.operators['icontains']


def get_prep_lookup(self, lookup_type, value):
    try:
        return self.get_prep_lookup_origin(lookup_type, value)
    except TypeError, e:
        if lookup_type in ('like', 'ilike'):
            return value
        raise e


def get_db_prep_lookup(self, lookup_type, value, *args, **kwargs):
    try:
        value_returned = self.get_db_prep_lookup_origin(lookup_type,
                                                        value,
                                                        *args, **kwargs)
    except TypeError, e:  # Django 1.1
        if lookup_type in ('like', 'ilike'):
            return [value]
        raise e
    if value_returned is None and lookup_type in ('like', 'ilike'):  # Dj > 1.1
        return [value]
    return value_returned


def monkey_get_db_prep_lookup(cls):
    cls.get_db_prep_lookup_origin = cls.get_db_prep_lookup
    cls.get_db_prep_lookup = get_db_prep_lookup
    if hasattr(subclassing, 'call_with_connection_and_prepared'):  # Dj > 1.1
        setattr(cls, 'get_db_prep_lookup',
        subclassing.call_with_connection_and_prepared(cls.get_db_prep_lookup))
        for new_cls in cls.__subclasses__():
            monkey_get_db_prep_lookup(new_cls)


monkey_get_db_prep_lookup(Field)
if hasattr(Field, 'get_prep_lookup'):
    Field.get_prep_lookup_origin = Field.get_prep_lookup
    Field.get_prep_lookup = get_prep_lookup
