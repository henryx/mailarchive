"""
Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
Project       mailarchive
Description   A mail archiver
License       GPL version 2 (see GPL.txt for details)
"""
import sqlite3


class Database:
    _connection = None

    @property
    def connection(self):
        return self._connection

    def __init__(self, location):
        self._connection = sqlite3.connect(location)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._connection:
                self._connection.commit()
                self._connection.close()
        except:
            pass
