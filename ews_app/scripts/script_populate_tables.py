from ews_app.tasks.populate_currencies import TaskPopulateCurrencies


def run():
    TaskPopulateCurrencies().populate()