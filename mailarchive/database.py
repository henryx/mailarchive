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
            self._createschema()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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

    def _createschema(self):
        """
        Create schema
        """
        pragmas = [
            "PRAGMA journal_mode=WAL"
        ]

        tables = [
            "CREATE TABLE headers(account, folder, received, fromaddr, toaddr, msgid)",
            "CREATE VIRTUAL TABLE messages USING FTS5(msgid, body)"
        ]

        with closing(self.connection.cursor()) as cur:
            for pragma in pragmas:
                cur.execute(pragma)

            for table in tables:
                cur.execute(table)

            self.connection.commit()

    def close(self):
        try:
            if self._connection:
                self._connection.commit()
                self._connection.close()
        except:
            pass

    def _store_headers(self, cursor, account, folder, mail):
        query = "INSERT INTO headers VALUES(?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (account, folder, mail["Date"], mail["From"], mail["To"], mail["Message-Id"]))

    def _store_body(self, cursor, mail):
        query = "INSERT INTO messages VALUES(?, ?)"

        if mail.is_multipart():
            body = ""
            for part in mail.walk():
                content = part.get_content_type()
                disposition = str(part.get('Content-Disposition'))

                if content == 'text/plain' and 'attachment' not in disposition:
                    body = part.get_payload(decode=True)
                    break
        else:
            body = mail.get_payload(decode=True)

        cursor.execute(query, (mail["Message-Id"], body))

    def store(self, account, folder, mail):
        with closing(self.connection.cursor()) as cur:
            self._store_headers(cur, account, folder[2], mail)
            self._store_body(cur, mail)
