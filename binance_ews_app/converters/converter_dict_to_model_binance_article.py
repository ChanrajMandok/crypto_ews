from singleton_decorator import singleton

from binance_ews_app.converters import logger
from binance_ews_app.model.model_binance_article_raw import ModelBinanceArticleRaw


@singleton
class ConverterDictToModelBinanceArticle:

    def convert(self, binance_article_dict: dict) -> ModelBinanceArticleRaw:
        try:
            binance_raw_article_object = ModelBinanceArticleRaw(
                id=binance_article_dict.get('id'),
                code=binance_article_dict.get('code'),
                title=binance_article_dict.get('title'),
                release_date=binance_article_dict.get('releaseDate')
            )
            return binance_raw_article_object

        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")