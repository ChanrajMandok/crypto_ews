import abc


class ConverterDictToModelArticleRawInterface(metaclass=abc.ABCMeta):
    """
    ConverterDictToModelArticleRaw:

    This class serves as the abstract base class for all converters.
    
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))
    
    @abc.abstractmethod
    def model_article_raw(self):
        raise NotImplementedError   
    
    @abc.abstractmethod
    def class_name(self) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        raise NotImplementedError
    
    @abc.abstractproperty
    def key_id(self) -> str:
        raise NotImplementedError

    @abc.abstractproperty
    def key_code(self) -> str:
        raise NotImplementedError
        
    @abc.abstractproperty
    def key_title(self) -> str:
        raise NotImplementedError
        
    @abc.abstractproperty
    def key_release_date(self) -> str:
        raise NotImplementedError
    
    @abc.abstractproperty
    def url(self) -> str:
        raise NotImplementedError
    
    
    def convert(self, article_dict: dict) -> model_article_raw:
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
            raw_article_object = \
                self.model_article_raw()(
                                        id           = article_dict.get(self.key_id),
                                        code         = article_dict.get(self.key_code),
                                        title        = article_dict.get(self.key_title),
                                        release_date = article_dict.get(self.key_release_date), 
                                        url          = article_dict.get(self.url)
                                        )
                
            return raw_article_object

        except Exception as e:
            # Logging the exception details, including the class name for clarity.
            self.logger_instance.error(f"{self.class_name} - ERROR: {e}")