from django.db import models


class ModelBinanceArticleRaw(models.Model):

    release_date       = models.BigIntegerField(null=False)
    title              = models.CharField(max_length=200, null=False)
    code               = models.CharField(max_length=100 , null=False)
    id                 = models.BigIntegerField(primary_key=True, null=False)

    class Meta:
        managed = False

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id}"