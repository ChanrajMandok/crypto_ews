from django.db import models

from ews_app.enum.enum_priority import EnumPriority
from binance_ews_app.model.model_binance_article_raw import ModelBinanceArticleRaw
from ews_app.enum.enum_low_alert_warning_key_words import EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import EnumHighAlertWarningKeyWords


class ModelBinanceArticle(models.Model):

    alert_priority   = models.CharField(max_length=50, choices=EnumPriority.choices(), null=True)
    article          = models.OneToOneField(ModelBinanceArticleRaw, on_delete=models.CASCADE, primary_key=True)
    alert_category   = models.CharField(max_length=50, choices=EnumLowAlertWarningKeyWords.choices() + EnumHighAlertWarningKeyWords.choices(), null=True)
        
    class Meta:
        managed = False

    def __repr__(self):
        return f"{self.__class__.__name__} {self.article.title}"
    


