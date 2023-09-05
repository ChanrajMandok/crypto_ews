from django.db import models

from binance_ews_app.model.model_binance_article_raw import \
                                        ModelBinanceArticleRaw
from ews_app.model_interfaces.model_article_interface import \
                                         ModelArticleInterface


class ModelBinanceArticle(ModelArticleInterface):

    raw_article = models.OneToOneField(ModelBinanceArticleRaw, on_delete=models.CASCADE)

    class Meta:
        managed = False

