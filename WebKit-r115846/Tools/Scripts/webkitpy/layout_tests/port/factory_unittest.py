# Copyright (C) 2010 Google Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest

from webkitpy.tool.mocktool import MockOptions
from webkitpy.common.system.systemhost_mock import MockSystemHost

from webkitpy.layout_tests.port import chromium_linux
from webkitpy.layout_tests.port import chromium_mac
from webkitpy.layout_tests.port import chromium_win
from webkitpy.layout_tests.port import factory
from webkitpy.layout_tests.port import google_chrome
from webkitpy.layout_tests.port import gtk
from webkitpy.layout_tests.port import mac
from webkitpy.layout_tests.port import qt
from webkitpy.layout_tests.port import test
from webkitpy.layout_tests.port import win


class FactoryTest(unittest.TestCase):
    """Test that the factory creates the proper port object for given combination of port_name, host.platform, and options."""
    # FIXME: The ports themselves should expose what options they require,
    # instead of passing generic "options".

    def setUp(self):
        self.webkit_options = MockOptions(pixel_tests=False)

    def assert_port(self, port_name=None, os_name=None, os_version=None, options=None, cls=None):
        host = MockSystemHost(os_name=os_name, os_version=os_version)
        port = factory.PortFactory(host).get(port_name, options=options)
        self.assertTrue(isinstance(port, cls))

    def test_mac(self):
        self.assert_port(port_name='mac-leopard', cls=mac.MacPort)
        self.assert_port(port_name='mac-leopard-wk2', cls=mac.MacPort)
        self.assert_port(port_name='mac', os_name='mac', os_version='leopard', cls=mac.MacPort)
        self.assert_port(port_name=None,  os_name='mac', os_version='leopard', cls=mac.MacPort)

    def test_win(self):
        self.assert_port(port_name='win-xp', cls=win.WinPort)
        self.assert_port(port_name='win-xp-wk2', cls=win.WinPort)
        self.assert_port(port_name='win', os_name='win', os_version='xp', cls=win.WinPort)
        self.assert_port(port_name=None, os_name='win', os_version='xp', cls=win.WinPort)
        self.assert_port(port_name=None, os_name='win', os_version='xp', options=self.webkit_options, cls=win.WinPort)

    def test_google_chrome(self):
        self.assert_port(port_name='google-chrome-linux32',
                         cls=google_chrome.GoogleChromeLinux32Port)
        self.assert_port(port_name='google-chrome-linux64', os_name='linux', os_version='lucid',
                         cls=google_chrome.GoogleChromeLinux64Port)
        self.assert_port(port_name='google-chrome-linux64',
                         cls=google_chrome.GoogleChromeLinux64Port)
        self.assert_port(port_name='google-chrome-win-xp',
                         cls=google_chrome.GoogleChromeWinPort)
        self.assert_port(port_name='google-chrome-win', os_name='win', os_version='xp',
                         cls=google_chrome.GoogleChromeWinPort)
        self.assert_port(port_name='google-chrome-win-xp', os_name='win', os_version='xp',
                         cls=google_chrome.GoogleChromeWinPort)
        self.assert_port(port_name='google-chrome-mac', os_name='mac', os_version='leopard',
                         cls=google_chrome.GoogleChromeMacPort)
        self.assert_port(port_name='google-chrome-mac-leopard', os_name='mac', os_version='leopard',
                         cls=google_chrome.GoogleChromeMacPort)
        self.assert_port(port_name='google-chrome-mac-leopard',
                         cls=google_chrome.GoogleChromeMacPort)

    def test_gtk(self):
        self.assert_port(port_name='gtk', cls=gtk.GtkPort)

    def test_qt(self):
        self.assert_port(port_name='qt', cls=qt.QtPort)

    def test_chromium_mac(self):
        self.assert_port(port_name='chromium-mac-leopard', cls=chromium_mac.ChromiumMacPort)
        self.assert_port(port_name='chromium-mac', os_name='mac', os_version='leopard',
                         cls=chromium_mac.ChromiumMacPort)
        self.assert_port(port_name='chromium', os_name='mac', os_version='leopard',
                         cls=chromium_mac.ChromiumMacPort)

    def test_chromium_linux(self):
        self.assert_port(port_name='chromium-linux', cls=chromium_linux.ChromiumLinuxPort)
        self.assert_port(port_name='chromium', os_name='linux', os_version='lucid',
                         cls=chromium_linux.ChromiumLinuxPort)

    def test_chromium_win(self):
        self.assert_port(port_name='chromium-win-xp', cls=chromium_win.ChromiumWinPort)
        self.assert_port(port_name='chromium-win', os_name='win', os_version='xp',
                         cls=chromium_win.ChromiumWinPort)
        self.assert_port(port_name='chromium', os_name='win', os_version='xp',
                         cls=chromium_win.ChromiumWinPort)

    def test_unknown_specified(self):
        self.assertRaises(NotImplementedError, factory.PortFactory(MockSystemHost()).get, port_name='unknown')

    def test_unknown_default(self):
        self.assertRaises(NotImplementedError, factory.PortFactory(MockSystemHost(os_name='vms')).get)


if __name__ == '__main__':
    unittest.main()
