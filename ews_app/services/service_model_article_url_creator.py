from ews_app.enum.enum_source import EnumSource
from ews_app.model_interfaces.model_article_raw_interface import \
                                          ModelArticleRawInterface


class ServiceModelArticleUrlCreator:

    @staticmethod
    def create_url(base_url: str,
                   source: EnumSource.choices(),
                   instance: ModelArticleRawInterface):
        
        code = instance.code
        title = instance.title.strip().replace(' ', '-')

        if source == EnumSource.BINANCE:
            final_url = base_url + code

        if source == EnumSource.OKX:
            final_url = instance.url

        return final_url
    
    @staticmethod
    def create_backup_url(base_url: str,
                          source: EnumSource.choices(),
                          instance: ModelArticleRawInterface):
        
        code = instance.code
        title = instance.title.strip().replace(' ', '-')
        
        if source == EnumSource.BINANCE:
            final_url = {base_url}-{title}-{code}

        if source == EnumSource.OKX:
            final_url = base_url + title.lower()


        return final_url