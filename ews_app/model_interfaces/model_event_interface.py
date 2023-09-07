from django.db import models
from django.contrib.postgres.fields import ArrayField

from ews_app.enum.enum_source import EnumSource
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_low_alert_warning_key_words import \
                                 EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                 EnumHighAlertWarningKeyWords


class ModelEventInterface(models.Model):

    id                 = models.IntegerField(null=False, primary_key=True)
    trading_affected   = models.BooleanField(default=False)
    url                = models.URLField(max_length=300, null=False)
    title              = models.CharField(max_length=300, null=False)
    release_date       = models.BigIntegerField(null=False, )
    alert_priority     = models.CharField(max_length=30, choices=EnumPriority.choices())
    h_spot_tickers     = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    h_usdm_tickers     = ArrayField(models.CharField(max_length=200), blank=True, default=list) 
    l_spot_tickers     = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    l_usdm_tickers     = ArrayField(models.CharField(max_length=50), blank=True, default=list) 
    important_dates    = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    network_tokens     = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    source             = models.CharField(max_length=50, choices=EnumSource.choices(), null=True)
    alert_category     = models.CharField(max_length=50, choices=EnumLowAlertWarningKeyWords.choices() \
                                                                + EnumHighAlertWarningKeyWords.choices())
    ms_teams_message   = models.JSONField(null=True)
    event_completed    = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"{self.__class__.__name__} Category: {self.alert_category.name}, Priotity: {self.alert_priority.value} "