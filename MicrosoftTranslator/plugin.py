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

import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring

from local import api

_ = PluginInternationalization('MicrosoftTranslator')

@internationalizeDocstring
class MicrosoftTranslator(callbacks.Plugin):
    """Add the help for "@plugin help MicrosoftTranslator" here
    This should describe *how* to use this plugin."""

    threaded = True

    def __init__(self, irc):
        self.__parent = super(MicrosoftTranslator, self)
        self.__parent.__init__(irc)

        self.engine = api.MicrosoftTranslator(self.registryValue('azureKey'))

    def translate(self, irc, msg, args, from_lang, to_lang, text):
        """<from-language> [to] <to-language> <text>

        Returns <text> translated from <from-language> into <to-language>.
        from-language can be "auto" for autodetection.
        """

        if from_lang not in self.engine.languages:
            irc.errorInvalid(_('Source language'), from_lang,
                format(_('Valid languages are %L'), engine.languages))

        if to_lang not in self.engine.languages:
            irc.errorInvalid(_('Destination language'), to_lang,
                format(_('Valid languages are: %L'), engine.languages))

        irc.reply(self.engine.translate(source=from_lang, target=to_lang,
            text=text))

    def detectlanguage(self, irc, msg, args, text):
        """ <text>

        Detects language of <text>.
        """

        irc.reply(self.engine.detect(text))

    translate = wrap(translate)
    detect = wrap(detectlanguage)


Class = MicrosoftTranslator


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
