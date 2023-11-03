from django.db import models
from ews_app.enum.enum_priority import EnumPriority
from ews_app.model.model_stablecoin import ModelStableCoin
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords


class ModelDefiStablecoin(models.Model):

    price                = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    release_date         = models.BigIntegerField(null=True)
    trading_affected     = models.BooleanField(default=False)
    mechanism            = models.CharField(null=True)
    stablecoin           = models.OneToOneField(ModelStableCoin, on_delete=models.CASCADE)
    peg_deviation        = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    one_day_price_change = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    url                  = models.URLField(max_length=200, null=True)
    alert_priority       = models.CharField(max_length=50, choices=EnumPriority.choices(), null=True)
    alert_category       = models.CharField(max_length=50, choices=EnumLowAlertWarningKeyWords.choices() \
                                                   + EnumHighAlertWarningKeyWords.choices(), null=True)
    
    
    class Meta:
        managed = False

    def __repr__(self):
        return f"{self.__class__.__name__} {self.alert_category.name}: {self.stablecoin.currency} "