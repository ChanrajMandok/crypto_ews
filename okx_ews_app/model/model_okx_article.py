from django.db import models

from okx_ews_app.model.model_okx_article_raw import \
                                        ModelOkxArticleRaw
from ews_app.model_interfaces.model_article_interface import \
                                         ModelArticleInterface


class ModelOkxArticle(ModelArticleInterface):

    raw_article = models.OneToOneField(ModelOkxArticleRaw, on_delete=models.CASCADE)

    class Meta:
        managed = False
