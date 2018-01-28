"""
Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
Project       mailarchive
Description   A mail archiver
License       GPL version 2 (see GPL.txt for details)
"""

import imaplib


class IMAP(object):
    """
    Class used to manage connection to IMAP server
    """
    _host = None
    _port = None
    _user = None
    _password = None
    _scheme = None
    _connection = None

    def __init__(self):
        pass

    @property
    def host(self):
        """
        Hostname property
        """
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @host.deleter
    def host(self):
        del self._host

    @property
    def port(self):
        """
        Port property
        """
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @port.deleter
    def port(self):
        del self._port

    @property
    def user(self):
        """
        User property
        """
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @user.deleter
    def user(self):
        del self._user

    @property
    def password(self):
        """
        Password property
        """
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @password.deleter
    def password(self):
        del self._password

    @property
    def scheme(self):
        """
        Scheme property
        """
        return self._scheme

    @scheme.setter
    def scheme(self, scheme):
        if scheme not in ["imap", "imaps"]:
            raise TypeError("scheme not supported: {}".format(scheme))
        self._scheme = scheme

    @scheme.deleter
    def scheme(self):
        del self._scheme

    def open(self):
        """
        Open connection to server
        """
        try:
            if self.scheme == "imap":
                self._connection = imaplib.IMAP4(
                    self.host, self.port)
            else:
                self._connection = imaplib.IMAP4_SSL(
                    self.host, self.port)
        except Exception as e:
            raise

    def close(self):
        """
        Close connection to the server
        """
        try:
            if self._connection:
                self._connection.close()
                self._connection.logout()
        except:
            pass

    def folders(self, folder="inbox"):
        """
        List folder in IMAP account
        :param folder: Folder that start to list
        :return: A tuple with result of operation and a list with folders extracted
        """
        self._connection.select(folder)
        tree = self._connection.list()

        return tree
