"""
Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
Project       mailarchive
Description   A mail archiver
License       GPL version 2 (see GPL.txt for details)
"""
import sqlite3
from contextlib import closing


class Database:
    _connection = None

    @property
    def connection(self):
        return self._connection

    def __init__(self, location):
        self._connection = sqlite3.connect(location)

        if not self._checkschema():
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._connection:
                self._connection.commit()
                self._connection.close()
        except:
            pass

    def _checkschema(self):
        """
        Check schema existence
        :return: True if schema populated, else False
        """
        with closing(self._connection.cursor()) as cur:
            cur.execute("SELECT count(*) FROM sqlite_master")
            res = cur.fetchone()[0]
            if res > 0:
                return True
            else:
                return False