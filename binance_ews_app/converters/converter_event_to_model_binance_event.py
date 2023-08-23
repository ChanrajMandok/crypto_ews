from singleton_decorator import singleton

from binance_ews_app.converters import logger
from binance_ews_app.model.model_binance_event import ModelBinanceEvent


@singleton
class ConverterEventToBinanceModelEvent:

    def convert(self, binance_article_object: dict) -> ModelBinanceEvent:
        try:
            binance_event = ModelBinanceEvent(
                id=binance_article_object.get('id'),
                code=binance_article_object.get('code'),
                title=binance_article_object.get('title'),
                release_date=binance_article_object.get('releaseDate'),
                alert_category=binance_article_object.get('Alert_Category'),
                alert_priority=binance_article_object.get('Alert_Priority'),
                url=binance_article_object.get('url'),
                important_dates=binance_article_object.get('important_dates', []),
                article=binance_article_object.get('article'),
                spot_pairs=binance_article_object.get('spot_pairs', []),
                usdm_pairs=binance_article_object.get('USDⓈ-M_pairs', [])
            )
            return binance_event

        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")