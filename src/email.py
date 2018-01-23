"""
Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
Project       mailarchive
Description   A mail archiver
License       GPL version 2 (see GPL.txt for details)
"""


class IMAP(object):
    _host = None

    def __init__(self):
        pass

    @property
    def host(self):
        """
        Hostname property
        :return Return the hostname
        """
        return self._host

    @host.getter
    def host(self, host):
        """
        Set the hostname property
        """
        self._host = host

    @host.deleter
    def host(self):
        """
        Delete the hostname property
        """
        del self._host
