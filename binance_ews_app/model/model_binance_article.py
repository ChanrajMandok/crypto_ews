from django.db import models

from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_low_alert_warning_key_words import \
                                 EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                 EnumHighAlertWarningKeyWords
from binance_ews_app.model.model_binance_article_raw import \
                                       ModelBinanceArticleRaw


class ModelBinanceArticle(models.Model):

    url              = models.URLField(max_length=200, null=True)
    html             = models.CharField(max_length=25000, null=True)
    id               = models.BigIntegerField(primary_key=True, null=False)
    raw_article      = models.OneToOneField(ModelBinanceArticleRaw, on_delete=models.CASCADE)
    alert_priority   = models.CharField(max_length=50, choices=EnumPriority.choices(), null=True)
    alert_category   = models.CharField(max_length=50, choices=EnumLowAlertWarningKeyWords.choices() \
                                                   + EnumHighAlertWarningKeyWords.choices(), null=True)
    
    class Meta:
        managed = False

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id}"
    


