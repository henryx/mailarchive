"""
Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
Project       mailarchive
Description   A mail archiver
License       GPL version 2 (see GPL.txt for details)
"""
import email
import sqlite3
from contextlib import closing

import bson
import pymongo


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
            "CREATE TABLE accounts(account, folder)",
            "CREATE TABLE headers(account, folder, headername, headervalue)",
            "CREATE VIRTUAL TABLE messages USING FTS5(account, msgid, body)"
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

    def _store_account(self, cursor, account, folder):
        query = "INSERT INTO accounts VALUES(?, ?)"
        cursor.execute(query, (account, folder))

    def _store_headers(self, cursor, account, folder, mail):
        query = "INSERT INTO headers VALUES(?, ?, ?, ?)"
        for header in mail:
            cursor.execute(query, (account, folder, header, mail[header]))

    def _store_body(self, cursor, account, mail):
        query = "INSERT INTO messages VALUES(?, ?, ?)"

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

        cursor.execute(query, (account, mail["Message-Id"], body))

    def exists(self, account, folder, mail):
        """
        Check if email is already stored for account
        :param account: Account name
        :param folder: Folder that contain the email
        :param mail: The email
        :return: True if is already stored else False
        """

        query = "SELECT Count(*) FROM headers WHERE account = ? AND folder = ? AND Upper(headername) = ? AND headervalue = ?"

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, (account, folder, "Message-Id".upper(), mail["Message-Id"]))
            counted = cursor.fetchone()[0]

        if counted > 0:
            return True
        else:
            return False

    def store(self, account, folder, mail):
        if not self.exists(account, folder[2], mail):
            with closing(self.connection.cursor()) as cur:
                self._store_account(cur, account, folder[2])
                self._store_headers(cur, account, folder[2], mail)
                self._store_body(cur, account, mail)


class MongoDB:
    _connection = None

    @property
    def connection(self):
        return self._connection

    def __init__(self, cfg):
        host = cfg["host"]
        port = cfg["port"] if "port" in cfg else 27017
        user = cfg["user"] if "user" in cfg else None
        password = cfg["password"] if "password" in cfg else None
        dbauth = cfg["dbauth"] if "dbauth" in cfg else "admin"

        self._connection = pymongo.MongoClient(host=host,
                                               port=int(port),
                                               username=user,
                                               password=password,
                                               authSource=dbauth)

        self._database = self._connection[cfg["database"]]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._connection.close()

    def exists(self, account, folder, mail):
        """
        Check if email is already stored for account
        :param account: Account name
        :param folder: Folder that contain the email
        :param mail: The email
        :return: True if is already stored else False
        """

        collection = self._database["data"]

        data = {
            "account": account,
            "folder": folder,
            "headers": {
                "header": "Message-ID",
                "value": mail["Message-ID"]
            }
        }

        cur = collection.count(data)

        return False if cur == 0 else True

    def store(self, account, folder, mail):
        collection = self._database["data"]

        if not self.exists(account, folder[2], mail):
            return

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

        parser = email.parser.HeaderParser()
        headers = parser.parsestr(mail.as_string())

        data = {
            "account": account,
            "folder": folder[2],
            "headers": [dict(header=header, value=headers[header]) for header in headers],
            "body": body.decode(errors="replace") if type(body) == bytes else body
        }

        try:
            collection.insert_one(data)
        except bson.errors.InvalidDocument as e:
            print("|-- Cannot insert document: {}".format(e))
