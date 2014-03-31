import logging
import xmlrpclib

log = logging.getLogger(__name__)

class RemoteException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ConfluenceXmlRpcHandler():
    def __init__(self, url, username=None, password=None, api_version=2):
        self._token = None
        self._username = username
        self._password = password
        self._server = xmlrpclib.ServerProxy(url + "/rpc/xmlrpc")
        self._api_version = api_version

        if self._api_version == 1:
            self._server_confluence = self._server.confluence1
        else:
            self._server_confluence = self._server.confluence2

    def login(self, username=None, password=None):
        """
        Logs in user. If successful, returns user token.
        """

        if username is not None:
            self._username = username
        if password is not None:
            self._password = password

        try:
            self._token = self._server_confluence.login(self._username, self._password)
        except xmlrpclib.Fault as e:
            raise RemoteException(e)

