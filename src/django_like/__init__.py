from django.db.models.fields import Field
from django.db.models.fields import subclassing
from django.db.models.sql.constants import QUERY_TERMS
from django.db.backends.sqlite3.base import DatabaseWrapper


QUERY_TERMS['like'] = None
QUERY_TERMS['ilike'] = None
DatabaseWrapper.operators['like'] = DatabaseWrapper.operators['contains']
DatabaseWrapper.operators['ilike'] = DatabaseWrapper.operators['icontains']


def get_prep_lookup(self, lookup_type, value):
    try:
        self.get_prep_lookup_origin(lookup_type, value)
    except TypeError, e:
        if lookup_type in ('like', 'ilike'):
            return value
        raise e


def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
    value_returned = self.get_db_prep_lookup_origin(lookup_type=lookup_type,
                                                    value=value,
                                                    connection=connection,
                                                    prepared=prepared)
    if value_returned is None and lookup_type in ('like', 'ilike'):
        return [value]
    return value


def monkey_get_db_prep_lookup(cls):
    cls.get_db_prep_lookup_origin = cls.get_db_prep_lookup
    cls.get_db_prep_lookup = get_db_prep_lookup
    setattr(cls, 'get_db_prep_lookup',
    subclassing.call_with_connection_and_prepared(cls.get_db_prep_lookup))
    for new_cls in cls.__subclasses__():
        monkey_get_db_prep_lookup(new_cls)


monkey_get_db_prep_lookup(Field)
Field.get_prep_lookup_origin = Field.get_prep_lookup
Field.get_prep_lookup = get_prep_lookup
