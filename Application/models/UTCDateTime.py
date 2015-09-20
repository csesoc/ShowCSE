import datetime
import pytz
from sqlalchemy import (
    Column,
    DateTime
)

from sqlalchemy import types


class UTCDateTime(types.TypeDecorator):

    impl = types.DateTime
    
    def process_bind_param(self, value, engine):
        if value is not None:
            return value.astimezone(pytz.UTC)

    def process_result_value(self, value, engine):
        if value is not None:
            return value.replace(tzinfo=pytz.UTC)

def now():
    return datetime.datetime.now(pytz.UTC)
