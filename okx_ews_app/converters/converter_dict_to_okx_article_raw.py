from okx_ews_app.converters import logger
from okx_ews_app.model.model_okx_article_raw import \
                                       ModelOkxArticleRaw
from ews_app.converter_interfaces.converter_dict_to_model_article_raw_interface \
                                    import ConverterDictToModelArticleRawInterface


class ConverterDictToModelokxArticleRaw(ConverterDictToModelArticleRawInterface):

    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance   = logger
        self._model_article_raw = ModelOkxArticleRaw

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def key_id(self) -> str:
        return 'sort'
        
    @property
    def key_code(self) -> str:
        return 'sort'

    @property
    def key_title(self) -> str:
        return 'shareTitle'

    @property
    def key_release_date(self) -> str:
        return 'publishDate'
    
    @property
    def logger_instance(self):
        return self._logger_instance

    def model_article_raw(self):
        return self._model_article_raw
