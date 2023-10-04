from decimal import Decimal
from ews_app.enum.enum_no_value_interface import NoValue


class EnumWarningPriceChange(NoValue):

    ONE_MINUTE          = Decimal(0.00)
    FIFTEEN_MINUTES     = Decimal(0.04)
    THIRTY_MINUTES      = Decimal(0.08)
    ONE_HOUR            = Decimal(0.1)
    SIX_HOURS           = Decimal(0.15)
    TWELVE_HOURS        = Decimal(0.15)
    TWENTY_FOUR_HOURS   = Decimal( 0.15)