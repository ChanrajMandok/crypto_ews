from django.db import models


class ModelWirexDepositCurrency(models.Model):
    
    id        = models.AutoField(primary_key=True)
    currency  = models.CharField(max_length=50, null=False)
    name      = models.CharField(max_length=50, null=False, default='test')