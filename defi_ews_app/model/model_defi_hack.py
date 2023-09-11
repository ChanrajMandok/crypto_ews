from ews_app.model_interfaces.model_hack_raw_interface \
                            import ModelHackRawInterface


class ModelDefiHack(ModelHackRawInterface):

    class Meta:
        managed = False