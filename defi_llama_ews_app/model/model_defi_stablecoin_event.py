from ews_app.model_interfaces.model_event_interface \
                           import ModelEventInterface


class ModelDefiStableCoinEvent(ModelEventInterface):

    class Meta:
        managed = True
        ordering = ['-release_date']