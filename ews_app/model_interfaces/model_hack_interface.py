from django.db import models

from ews_app.enum.enum_priority import EnumPriority
from django.contrib.postgres.fields import ArrayField
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                 EnumHighAlertWarningKeyWords


class ModelHackInterface(models.Model):

    hacked_amount_m  = models.FloatField(null=True)
    release_date     = models.BigIntegerField(null=True)
    trading_affected = models.BooleanField(default=False)
    url              = models.URLField(max_length=200, null=True)
    protocol         = models.CharField(max_length=30, null=True)
    exploit          = models.CharField(max_length=30, null=True)
    blockchain       = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    alert_priority   = models.CharField(max_length=50, choices=EnumPriority.choices(), null=True)
    alert_category   = models.CharField(max_length=50, choices=EnumLowAlertWarningKeyWords.choices() \
                                                   + EnumHighAlertWarningKeyWords.choices(), null=True)
    network_tokens   = ArrayField(models.CharField(max_length=200), blank=True, default=list)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"{self.__class__.__name__} {self.protocol} Hack"
    

