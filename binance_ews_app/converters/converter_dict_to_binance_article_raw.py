from binance_ews_app.converters import logger
from binance_ews_app.model.model_binance_article_raw import \
                                       ModelBinanceArticleRaw
from ews_app.converter_interfaces.converter_dict_to_model_article_raw_interface import \
                                                 ConverterDictToModelArticleRawInterface


class ConverterDictToBinanceArticleRaw(ConverterDictToModelArticleRawInterface):

    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance    = logger
        self._model_article_raw  = ModelBinanceArticleRaw

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def key_id(self) -> str:
        return 'id'
        
    @property
    def key_code(self) -> str:
        return 'code'

    @property
    def key_title(self) -> str:
        return 'title'

    @property
    def key_release_date(self) -> str:
        return 'releaseDate'
    
    @property
    def url(self) -> str:
        return None
    
    @property
    def logger_instance(self):
        return self._logger_instance

    def model_article_raw(self):
        return self._model_article_raw