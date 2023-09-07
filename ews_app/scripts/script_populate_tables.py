from ews_app.tasks.task_populate_currencies_from_env import TaskPopulateCurrenciesFromEnv
from ews_app.tasks.task_populate_currencies_from_wx_db import TaskpopulateCurrenciesFromWxDb

def run():
    TaskPopulateCurrenciesFromEnv().populate()
    TaskpopulateCurrenciesFromWxDb().populate()