from django.db import models


class ModelWirexUsdmCurrency(models.Model):
    
    id        = models.AutoField(primary_key=True)
    currency  = models.CharField(max_length=50, null=False)