"""Python wrapper for the AppAssure 5 REST API.

Provides an abstraction layer for using the AppAssure 5 API. Sends
well-formed XML requests through a given AppAssureSession object.
"""

import datetime

class AppAssureAPI(object):
    """Allows us to request data from the API as a logged-in user."""

    def __init__(self, session):
        """You MUST provide a valid AppAssureSession object as a
        parameter when creating a new AppAssureAPI object.
        """
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        """We don't want to close the AppAssureSession object, so there
        is nothing to do here.
        """
        pass

    def formatTime(self, time):
        """Convert a datetime object to a string in the format expected
        by the AppAssure API.
        """
        return time.isoformat()[:-3]+'Z'

    def deformatTime(self, string):
        """Convert a string in the format used by the AppAssure API to a
        datetime object.
        """
        return datetime.datetime.strptime(string[:-1],
                "%Y-%m-%dT%H:%M:%S.%f")

    def now(self):
        """Return the current time as a string in the format expected by
        the AppAssure API.
        """
        return self.formatTime(datetime.datetime.now())

    def _getXMLEndTag(self, starttag):
        """Deal with things like
        <string xmlns="http://apprecovery.com/management/api/2010/05">
        </string>
        """
        if ' ' in starttag:
            endtag = starttag.split(' ')[0]
        else:
            endtag = starttag
        return endtag

    def _getXML(self, data, objname=None):
        """Convert a Python object into XML in the format expected by
        the AppAssure server.

        Original source:
        http://code.activestate.com/recipes/440595-extensible-object-to-xml-convertor/

        This is an internal function, do not use it.
        """
        if type(data) == type(list()):
            # if data is a list
            xml = ""
            for item in data:
                xml += self._getXML(item, objname)
        elif type(data) == type(dict()):
            # if data is a dict
            xml = "<%s>" % objname
            for key, value in data.items():
                xml += self._getXML(value, key)
            xml += "</%s>" % self._getXMLEndTag(objname)
        else:
            # assume data is a str
            xml = '<%s>%s</%s>' % (objname, data, self._getXMLEndTag(objname))
        return xml

    def getXML(self, data, objname=None):
        """Convert a Python object into XML in the format expected by
        the AppAssure server.

        data should be a dict, and objname should be a string.
        """
        xml = self._getXML(data, '%s xmlns="http://apprecovery.com/management/api/2010/05"' %
                objname)
        return ('<?xml version="1.0" encoding="utf-8"?>' +
                    xml).encode('utf-8')