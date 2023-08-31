from django.db import models


class ModelDbBinanceLastUpdated(models.Model):

    last_updated = models.BigIntegerField(primary_key=True, null=False)

    class Meta:
        managed = False

    def __repr__(self):
        return f"{self.__class__.__name__} {self.last_updated}"