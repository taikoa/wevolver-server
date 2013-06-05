import datetime
from datetime import timedelta
from dateutil.tz import gettz

from django.utils import dateformat
from django.conf import settings
from tastypie.serializers import Serializer
from tastypie.utils import format_datetime, make_naive, now


class TzSerializer(Serializer):
    """
    A subclass of the built-in Serializer that adds timezone offsets to
    outputted times, making them ISO-8601 compliant.

    Based on the patch in this pull request:
    https://github.com/toastdriven/django-tastypie/pull/445
    """

    def __init__(self, formats=None, content_types=None, datetime_formatting=None):
        super(TzSerializer, self).\
            __init__(formats, content_types, datetime_formatting)
        timezone_str = getattr(settings, 'TIME_ZONE', None)
        if timezone_str:
            self.tzinfo = gettz(timezone_str)

    def format_datetime(self, data):
        """
        A hook to control how datetimes are formatted.

        Can be overridden at the ``Serializer`` level (``datetime_formatting``)
        or globally (via ``settings.TASTYPIE_DATETIME_FORMATTING``).

        Default is ``iso-8601``, which looks like "2010-12-16T03:02:14+00:00".
        """
        data = make_naive(data)
        if self.datetime_formatting == 'rfc-2822':
            return format_datetime(data)

        if self.tzinfo:
            data = datetime.datetime(data.year, data.month, data.day,\
                    data.hour, data.minute, data.second, data.microsecond,\
                    self.tzinfo)

            #return data.isoformat()
            return data


class DateSerializer(TzSerializer):
    def format_datetime(self, dt):
        date = super(DateSerializer, self).format_datetime(dt)
        return dateformat.format(date, 'Y-m-d')


class DatetimeSerializer(TzSerializer):
    def format_datetime(self, dt):
        date = super(DatetimeSerializer, self).format_datetime(dt)
        return dateformat.format(date, 'jS F Y - H:i')


class MomentSerializer(TzSerializer):
    def format_datetime(self, dt):
        date = super(MomentSerializer, self).format_datetime(dt)
        today = now()
        if today.day == date.day:
            return ' - '.join(['today', dateformat.format(date, 'H:i')])
        elif today - timedelta(days=1) == date:
            return ' - '.join(['yesterday', dateformat.format(date, 'H:i')])
        else:
            return dateformat.format(date, 'jS F Y - H:i')
