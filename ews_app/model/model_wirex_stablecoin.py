from django.db import models


class ModelWirexStableCoin(models.Model):
    
    id        = models.AutoField(primary_key=True)
    currency  = models.CharField(max_length=50, null=False)
    
    def __repr__(self):
        return f"{self.__class__.__name__} {self.currency} "