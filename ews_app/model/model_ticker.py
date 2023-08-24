from django.db import models
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_currency_type import EnumCurrencyType

class ModelTicker(models.Model):
    
    quote_currency     = models.CharField(max_length=50, null=False)
    base_currency      = models.CharField(max_length=50, null=False)
    name               = models.CharField(null=False, unique=True, max_length=100)
    alert_priority     = models.CharField(max_length=50, choices=EnumPriority.choices(), null=False)
    currency_type      = models.CharField(max_length=50, choices=EnumCurrencyType.choices(), null=False)
    
    class Meta:
        managed = False
        
    def __repr__(self):
        return f"{self.__class__.__name__} Category: {self.name}, Priotity: {self.alert_priority.value} "