from ews_app.model_interfaces.model_event_interface \
                           import ModelEventInterface


class ModelTokenLiquidityEvent(ModelEventInterface):

    class Meta:
        managed = True
        ordering = ['-release_date']