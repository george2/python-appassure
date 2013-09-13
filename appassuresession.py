"""Python wrapper for the AppAssure 5 REST API.

    AppAssureSession
    Handles logging in to and sending and retrieving data from an
    AppAssure core server. Returns requested data as a Python object.
"""

from xml2obj import xml2obj
import requests
from requests_ntlm import HttpNtlmAuth

# AppAssure 5 API Core URL
API_URL = "apprecovery/api/core/"
# Login URL (any page that returns a 200 OK response when logged in)
LOGIN_URL = "apprecovery/admin/Core"


# Exception classes used by AppAssureSession.
class LoginError(Exception):
    """Connecting and/or logging in to the AppAssure server failed."""


class UnsupportedMethodError(Exception):
    """An unsupported HTTP method was specified."""


class InvalidURIError(Exception):
    """An invalid URI was specified."""


class AppAssureSession(object):
    """Allows us to request data from the API as a logged-in user."""
    
    def __init__(self, host, port, username, password, domain='DOMAIN'):
        """The default domain of 'DOMAIN' is used because the AppAssure
           server does not seem to use this value at all. The optional
           argument is only provided in case your situation is
           different. (For example, if you use Active Directory, perhaps
           your AppAssure server will need to verify with a certain
           domain.
        """
        self.username = username
        self.baseurl = "https://%s:%s/" % (host, port)
        self.apiurl = self.baseurl + API_URL
        self.loginurl = self.baseurl + LOGIN_URL
        self.http = requests.Session()
        self.auth = HttpNtlmAuth('%s\\%s' % (domain, self.username),
                password)
        status = self.http.get(self.loginurl, verify=False,
                auth=self.auth)
        if not status.ok:
            raise LoginError("Connecting and/or logging in to the AppAssure server failed.",
                   status)

    def __enter__(self):
        return self

    def close(self):
        """End the session."""
        self.http.close()

    def __exit__(self, type, value, tb):
        self.close()

    def request(self, uri, method='GET', data=None):
        """Sends a request to the AppAssure Core server, with the
           specified uri. Returns a structured object containing the
           data from the server's response. The optional 'data'
           parameter is only used if the HTTP method supports sending
           data to the server. (Eg, POST.)

           method must be one of:
                GET, POST, PUT, DELETE
        """
        if method == 'GET':
            response = self.http.get("%s%s" % (self.apiurl, uri),
                    auth=self.auth)
        elif method == 'POST':
            response = self.http.post("%s%s" % (self.apiurl, uri), data,
                    auth=self.auth)
        elif method == 'PUT':
            response = self.http.put("%s%s" % (self.apiurl, uri), data,
                    auth=self.auth)
        elif method == 'DELETE':
            response = self.http.delete("%s%s" % (self.apiurl, uri),
                    auth=self.auth)
        else:
            raise UnsupportedMethodError("Unsupported HTTP method", method)

        if response.ok:
            return xml2obj(response.text)
        else:
            raise InvalidURIError("The server returned an error message.",
                   response, self.apiurl + uri)


