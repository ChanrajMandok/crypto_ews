from django.db import models

from ews_app.enum.


class ModelDefiHackInterface(models.Model):

    release_date       = models.BigIntegerField(null=False)
    title              = models.CharField(max_length=200, null=False)
    blockchain         = models.CharField(max_length=50, choices=EnumPriority.choices(), null=True)
    url                = models.URLField(max_length=300, null=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id}"