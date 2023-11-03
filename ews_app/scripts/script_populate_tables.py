from ews_app.tasks.task_populate_currencies_from_env import \
                                TaskPopulateCurrenciesFromEnv
from ews_app.tasks.task_populate_stablecoins_from_env import \
                                TaskPopulateStableCoinsFromEnv
from ews_app.tasks.task_populate_deposit_currencies_from_env import \
                                 TaskpopulateDepositCurrenciesFromEnv


def run():
    TaskPopulateCurrenciesFromEnv().populate()
    TaskPopulateStableCoinsFromEnv().populate()
    TaskpopulateDepositCurrenciesFromEnv().populate()