from decimal import Decimal
from django.db import models

from ews_app.enum.enum_source import EnumSource


class ModelQuote(models.Model):
    
    time     = models.IntegerField()
    price    = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    volume   = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    source   = models.CharField(max_length=50, choices=EnumSource.choices(), null=True)
    
    class Meta:
        managed = False
        