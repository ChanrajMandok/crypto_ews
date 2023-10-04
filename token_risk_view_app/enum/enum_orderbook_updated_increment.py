from datetime import timedelta 
from ews_app.enum.enum_no_value_interface import NoValue


class EnumOrderbookUpdatedIncrement(NoValue):

    ONE_MINUTE         = timedelta(minutes=1)- timedelta(seconds=15)
    FIFTEEN_MINUTES    = timedelta(minutes=15)- timedelta(seconds=15)
    THIRTY_MINUTES     = timedelta(minutes=30)- timedelta(seconds=15)
    ONE_HOUR           = timedelta(hours=1)- timedelta(seconds=15)
    SIX_HOURS          = timedelta(hours=6)- timedelta(seconds=15)
    TWELVE_HOURS       = timedelta(hours=12)- timedelta(seconds=15)
    TWENTY_FOUR_HOURS  = timedelta(hours=24)- timedelta(seconds=15)