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

        log.debug(self._server_confluence.__dict__)

        if username and password:
            self.login()

    def login(self, username=None, password=None):
        """
        Logs in user. If successful, returns user token.
        """

        if username is not None:
            self._username = username
        if password is not None:
            self._password = password

        log.debug("Log in: %s" % self._username)
        try:
            self._token = self._server_confluence.login(self._username, self._password)
        except xmlrpclib.Fault as e:
            raise RemoteException(e)

        log.debug("Token: %s" % self._token)
        return self._token

    def logout(self, token=None):
        if token is None:
            token = self._token

        log.debug("Logout token: %s" % token)
        try:
            status = self._server_confluence.logout(token)
        except xmlrpclib.Fault as e:
            raise RemoteException(e)

        if status and token == self._token:
            self._token = None

        log.debug("Logout status: %s" % status)
        return status

    def getToken(self):
        return self._token
