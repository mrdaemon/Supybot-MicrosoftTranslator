###
# Copyright (c) 2012, Alexandre Gauthier
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

""" Horrible mini API client for the Microsoft Translator Azure Data Service

https://datamarket.azure.com/dataset/1899a118-d202-492c-aa16-ba21c33c06cb
"""


import urllib
import urllib2
from xml.etree.ElementTree import ElementTree
import sys


SERVICEURL = \
    "https://api.datamarket.azure.com/Data.ashx/Bing/MicrosoftTranslator/"

class MicrosoftTranslator(object):
    """ Interface to the Microsoft Translator Azure Data Service """

    def __init__(self, azurekey):
        """ Construct MicrosoftTranslator, initialize opener """

        # Use Azure HTTP Basic authentication for OData query.
        # API requires any username and azure key as password
        authman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        authman.add_password(None, SERVICEURL, "foo", azurekey)

        handler = urllib2.HTTPBasicAuthHandler(authman)

        self.opener = urllib2.build_opener(handler)
        self._languages = []

    @property
    def languages(self):
        """ Get a list of supported languages """

        # Caching, only expensive on first call.
        if not len(self._languages):
            data = self._query("GetLanguagesForTranslation")
            self._languages = [lang.text for lang in data]

        return self._languages


    def translate(self, target, text, source=None):
        """ Translate `text` from language `source` into language `tolang`

        The source language can be ommited or set to None, it will
        then be autodetected.
        """

        if source is None:
            data = self._query("Translate", To=target, Text=text)
        else:
            data = self._query("Translate", From=source, To=target, Text=text)

        return data.text

    def detect(self, text):
        """ Detect the language of `text` """

        data = self._query("Detect", Text=text)
        return data.text


    def _query(self, method, top="100", fmt="Raw", **kwargs):
        """ Query Data Service with parameters

        Returns an ElementTree containing the data
        """

        args = ["%s=%s&" % (k,_enc(v)) for k,v in kwargs.iteritems()]
        args = "".join(args)
        url = SERVICEURL + method + "?" + args + "$top=%s&$format=%s" % (top, fmt)
        tree = ElementTree()
        data = []

        try:
            handle = self.opener.open(urllib2.Request(url))
            data = tree.parse(handle)
            handle.close()
        except IOError, ex:
            if hasattr(ex, 'read'):
                print >>sys.stderr, ex.read()
                raise
            else:
                print >>sys.stderr, str(ex)
                raise

        return data


def _enc(string):
    """ Produces a URL encoded version of string in singlequotes """

    return urllib.quote_plus("'%s'" % string)


