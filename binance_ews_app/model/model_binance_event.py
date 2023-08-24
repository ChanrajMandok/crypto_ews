from django.db import models
from django.contrib.postgres.fields import ArrayField

from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_low_alert_warning_key_words import \
    EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
    EnumHighAlertWarningKeyWords


class ModelBinanceEvent(models.Model):

    release_date       = models.BigIntegerField(null=False)
    url                = models.URLField(max_length=200, null=False)
    title              = models.CharField(max_length=100, null=False)
    article_text       = models.TextField(max_length=25000, null=False)
    id                 = models.IntegerField(null=False, primary_key=True)
    alert_priority     = models.CharField(max_length=50, choices=EnumPriority.choices())
    h_spot_currencies  = ArrayField(models.CharField(max_length=50), blank=True, default=list, null=True)
    h_usdm_currencies  = ArrayField(models.CharField(max_length=50), blank=True, default=list, null=True) 
    l_spot_currencies  = ArrayField(models.CharField(max_length=50), blank=True, default=list, null=True)
    l_usdm_currencies  = ArrayField(models.CharField(max_length=50), blank=True, default=list, null=True) 
    important_dates    = ArrayField(models.CharField(max_length=200), blank=True, default=list, null=True)
    alert_category     = models.CharField(max_length=50, choices=EnumLowAlertWarningKeyWords.choices() + EnumHighAlertWarningKeyWords.choices())

    class Meta:
        managed = False

    def __repr__(self):
        return f"{self.__class__.__name__} Category: {self.alert_category.name}, Priotity: {self.alert_priority.value} "