from ews_app.model_interfaces.model_hack_interface \
                            import ModelHackInterface


class ModelDefiLlamaBridgeHack(ModelHackInterface):

    class Meta:
        managed = False

    def __repr__(self):
        return f"{self.__class__.__name__} {self.protocol} Bridge Hack"