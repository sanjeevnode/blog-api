from datetime import datetime

import pytz
from sqlalchemy import DateTime, TypeDecorator
from sqlalchemy.engine import Dialect

from app.core.config import settings


class ISTDateTime(TypeDecorator):
    """Custom SQLAlchemy type that saves and loads all datetime values as timezone-aware IST datetimes."""

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        """Converts datetime to IST before saving it to the database."""
        if value is None:
            return None
        ist_tz = pytz.timezone(settings.TIMEZONE)
        if value.tzinfo is None:
            return ist_tz.localize(value)
        return value.astimezone(ist_tz)

    def process_result_value(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        """Attaches the IST timezone to the datetime when reading from the database."""
        if value is None:
            return None
        ist_tz = pytz.timezone(settings.TIMEZONE)
        if value.tzinfo is None:
            return ist_tz.localize(value)
        return value.astimezone(ist_tz)
