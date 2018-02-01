"""
Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
Project       mailarchive
Description   A mail archiver
License       GPL version 2 (see GPL.txt for details)
"""

import imaplib
import re


class IMAPFolders(object):
    """
    Class iterator used for returning a tuple contains IMAP folder attributes,
    IMAP folder separator and IMAP folder name
    """
    _data = None
    _pattern = None
    _index = 0

    def __init__(self, data):
        self._data = data
        self._pattern = re.compile(
            r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

    def __iter__(self):
        return self

    def __next__(self):
        try:
            flags, delimiter, mailbox_name = self._pattern.match(
                self._data[self._index].decode()).groups()
        except IndexError:
            raise StopIteration

        mailbox_name = mailbox_name.strip('"')

        self._index += 1
        return (flags, delimiter, mailbox_name)


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
                self._connection.login(self.user, self.password)
        except imaplib.IMAP4.error as e:
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
        :return: The status of the operation and an iterator that contains the folder tree
        """
        self._connection.select(folder)
        status, tree = self._connection.list()

        folders = IMAPFolders(tree)

        return status, folders

    def count(self, folder="inbox"):
        """
        Count messages in folder (default INBOX)
        :param folder: Folder to count
        :return: The status of the operation and  counted messages in folder
        """
        status, counted = self._connection.select(folder)
        
        if status == "OK":
            return status, int(counted[0].decode())
        else:
            return status, -1
