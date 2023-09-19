from django.db import models

from ews_app.enum.enum_source import EnumSource
from ews_app.model.model_quote import ModelQuote


class ModelOrderBookLevel1(models.Model):
    
    ask    = models.ForeignKey(ModelQuote, on_delete=models.CASCADE, null=False, related_name="order_book_level_1_ask") 
    bid    = models.ForeignKey(ModelQuote, on_delete=models.CASCADE, null=False, related_name="order_book_level_1_bids") 
    source = models.CharField(max_length=50, choices=EnumSource.choices(), null=True)
    
    class Meta:
        managed = False
