"""
Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
Project       mailarchive
Description   A mail archiver
License       GPL version 2 (see GPL.txt for details)
"""


class IMAP(object):
    """
    Class used to manage connection to IMAP server
    """
    _host = None
    _port = None
    _user = None
    _password = None

    def __init__(self):
        pass

    @property
    def host(self):
        """
        Hostname property
        """
        return self._host

    @host.getter
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
