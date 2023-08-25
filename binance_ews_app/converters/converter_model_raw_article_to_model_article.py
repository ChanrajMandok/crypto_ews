from typing import Union

from binance_ews_app.converters import logger
from ews_app.enum.enum_priority import EnumPriority
from binance_ews_app.model.model_binance_article import \
                                       ModelBinanceArticle
from ews_app.enum.enum_low_alert_warning_key_words import \
                                 EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from binance_ews_app.model.model_binance_article_raw import \
                                        ModelBinanceArticleRaw


class ConverterModelRawArticleToModelArticle:

    def convert(self, 
                alert_priority: EnumPriority,
                model_raw_article: ModelBinanceArticleRaw,
                alert_category: Union[EnumLowAlertWarningKeyWords, 
                                      EnumHighAlertWarningKeyWords]):
        """
        Converts a raw article by adding alert_priority and alert_category
        to create/update an instance of ModelBinanceArticle.

        :param raw_article: An instance of ModelBinanceArticleRaw.
        :param alert_priority: The priority value to set.
        :param alert_category: The category value to set.
        :return: An instance of ModelBinanceArticle.
        """

        try:
            binance_article_object \
                        = ModelBinanceArticle(
                                            raw_article=model_raw_article,
                                            alert_category=alert_category, 
                                            alert_priority=alert_priority,
                                            id=model_raw_article.id
                                            )
            return binance_article_object

        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")