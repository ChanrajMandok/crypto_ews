from ews_app.tasks.task_populate_currencies_from_env import TaskPopulateCurrenciesFromEnv


def run():
    TaskPopulateCurrenciesFromEnv().populate()