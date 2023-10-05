from django.db import models

from ews_app.enum.enum_source import EnumSource
from ews_app.model.model_quote import ModelQuote


class ModelOrderBook(models.Model):

    symbol        = models.CharField(max_length=30, null=False)
    ask           = models.ForeignKey(ModelQuote, on_delete=models.CASCADE, null=False, related_name="order_book_level_1_ask") 
    bid           = models.ForeignKey(ModelQuote, on_delete=models.CASCADE, null=False, related_name="order_book_level_1_bids") 
    source        = models.CharField(max_length=50, choices=EnumSource.choices(), null=False)
    source_symbol = models.CharField(max_length=50, choices=EnumSource.choices(), null=False)
    
    class Meta:
        managed = False
