from ews_app.enum.enum_no_value_interface import NoValue


class EnumHighAlertWarningKeyWords(NoValue):
    # high priority
    CONGESTION                = 'congestion'
    SUSPENDED                 = 'suspended'
    SUSPENSION                = 'suspension'
    MIGRATION                 = 'migration'
    SWAP                      = 'swap'
    DELIST                    = 'delist'
    HARD                      = 'hard'
    FORK                      = 'fork'
    CEASE                     = 'cease'
    REMOVAL                   = 'removal'
    
    # low priority
    CONTRACT                  = 'contract'
    PROTOCOL                  = 'protocol'
    NETWORK                   = 'network'
    UPGRADE                   = 'upgrade'
