from datetime import timedelta 
from ews_app.enum.enum_no_value_interface import NoValue


class EnumOrderbookUpdatedIncrement(NoValue):

    ONE_MINUTE         = timedelta(minutes=1)
    FIFTEEN_MINUTES    = timedelta(minutes=15)
    THIRTY_MINUTES     = timedelta(minutes=30)
    ONE_HOUR           = timedelta(hours=1)
    SIX_HOURS          = timedelta(hours=6)
    TWELVE_HOURS       = timedelta(hours=12)
    TWENTY_FOUR_HOURS  = timedelta(hours=24)