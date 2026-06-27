import datetime
import pytz
from app.core.config import settings

def get_ist_now() -> datetime.datetime:
    """Get current time in IST (Indian Standard Time)"""
    utc_now = datetime.datetime.now(pytz.utc)
    ist_utc = pytz.timezone(settings.TIMEZONE)
    return utc_now.astimezone(ist_utc)
    