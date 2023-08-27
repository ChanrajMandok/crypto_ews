from binance_ews_app.converters import logger
from binance_ews_app.model.model_binance_article_raw import \
                                       ModelBinanceArticleRaw


class ConverterDictToModelBinanceArticleRaw:
    """
    ConverterDictToModelBinanceArticleRaw:
    
    This class is responsible for converting a dictionary containing details
    of a Binance article into a `ModelBinanceArticleRaw` object.

    """

    def convert(self, article_dict: dict) -> ModelBinanceArticleRaw:
        """
        Convert the provided dictionary into a ModelBinanceArticleRaw object.

        This method will attempt to extract specific keys from the provided
        dictionary and use their values to instantiate a `ModelBinanceArticleRaw`
        object.If any key is missing or if there's an exception during instantiation,
        an error will be logged, and the method will return None.

        Returns:
            ModelBinanceArticleRaw: An object representation of the Binance article. 
                                    Returns None if there was an error during conversion.

        """

        try:
            binance_raw_article_object = ModelBinanceArticleRaw(
                id           = article_dict.get('id'),
                code         = article_dict.get('code'),
                title        = article_dict.get('title'),
                release_date = article_dict.get('releaseDate')
            )
            
            return binance_raw_article_object

        except Exception as e:
            # Logging the exception details, including the class name for clarity.
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")
