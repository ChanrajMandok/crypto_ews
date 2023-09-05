from django.db import models


class ModelDbLastUpdatedInterface(models.Model):

    last_updated = models.BigIntegerField(primary_key=True, null=False)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"{self.__class__.__name__} {self.last_updated}"