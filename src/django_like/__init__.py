from django.db import backend
from django.db import connection
from django.db.models.fields import Field, subclassing
from django.db.models.sql.constants import QUERY_TERMS


QUERY_TERMS['like'] = None
QUERY_TERMS['ilike'] = None
connection.operators['like'] = connection.operators['contains']
connection.operators['ilike'] = connection.operators['icontains']
NEW_LOOKUP_TYPE = ('like', 'ilike')


def get_prep_lookup(self, lookup_type, value):
    try:
        return self.get_prep_lookup_origin(lookup_type, value)
    except TypeError, e:
        if lookup_type in NEW_LOOKUP_TYPE:
            return value
        raise e


def get_db_prep_lookup(self, lookup_type, value, *args, **kwargs):
    try:
        value_returned = self.get_db_prep_lookup_origin(lookup_type,
                                                        value,
                                                        *args, **kwargs)
    except TypeError, e:  # Django 1.1
        if lookup_type in NEW_LOOKUP_TYPE:
            return [value]
        raise e
    if value_returned is None and lookup_type in NEW_LOOKUP_TYPE:  # Dj > 1.1
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


def lookup_cast(self, lookup_type):
    lookup = '%s'
    if lookup_type == 'ilike':
        return 'UPPER(%s)' % lookup
    return self.lookup_cast_origin(lookup_type)


def monkey_ilike():
    backend_name = backend.__name__
    if 'postgres' in backend_name or \
      'postgres' in backend_name:
        connection.ops.__class__.lookup_cast_origin = connection.ops.lookup_cast
        connection.ops.__class__.lookup_cast = lookup_cast

monkey_get_db_prep_lookup(Field)
monkey_ilike()
if hasattr(Field, 'get_prep_lookup'):
    Field.get_prep_lookup_origin = Field.get_prep_lookup
    Field.get_prep_lookup = get_prep_lookup
