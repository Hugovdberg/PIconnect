''' AFSDK
    Loads the .NET libraries from the OSIsoft AF SDK
'''
# Copyright 2017 Hugo van den Berg, Stijn de Jong

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str,
                      ascii, chr, hex, input, next, oct, open,
                      pow, round, super,
                      filter, map, zip)
import sys
import os

import clr

# Get the installation directory from the environment variable or fall back to the Windows
# default installation path
PIAF_SDK = os.getenv('PIHOME', 'C:\\Program Files\\PIPC')
PIAF_SDK += '\\AF\\PublicAssemblies\\4.0\\'
if not os.path.isdir(PIAF_SDK):
    raise ImportError('PIAF SDK not found in %s, check installation' % PIAF_SDK)

sys.path.append(PIAF_SDK)
clr.AddReference('OSIsoft.AFSDK')  # pylint: disable=no-member

from OSIsoft import AF  # pylint: disable=import-error, wrong-import-position
