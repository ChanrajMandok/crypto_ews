from binance_ews_app.converters import logger
from binance_ews_app.model.model_binance_article_raw import \
    ModelBinanceArticleRaw


class ConverterDictToModelBinanceArticleRaw:

    def convert(self, article_dict: dict) -> ModelBinanceArticleRaw:
        
        try:
            binance_raw_article_object = ModelBinanceArticleRaw(
                id           = article_dict.get('id'),
                code         = article_dict.get('code'),
                title        = article_dict.get('title'),
                release_date = article_dict.get('releaseDate')
            )
            
            return binance_raw_article_object

        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")