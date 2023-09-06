import os
import pyodbc

from ews_app.services import logger
from singleton_decorator import singleton


@singleton
class ServiceWxAnalyticsConnectionRetriever:

    def __init__(self):
        self.wirex_pyodbc_connection = None

    def get_wirex_pyodbc_connection(self):

        if self.wirex_pyodbc_connection is None:
            try:
                self.wirex_pyodbc_connection = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                                                            "SERVER=wx-analytics.database.windows.net;"
                                                            "PORT=1433;"
                                                            "DATABASE=wx-analytics;"
                                                            "UID=" + os.environ["WIREX_LOGIN"] + ";"
                                                            "PWD=" + os.environ["WIREX_PASSWORD"] + ";"
                                                            "Authentication=ActiveDirectoryInteractive")
            except Exception as e:
                logger.error(f"{self.__class__.__name__} - ERROR {e}")

        return self.wirex_pyodbc_connection
    