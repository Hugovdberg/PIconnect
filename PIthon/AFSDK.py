''' AFSDK
    Loads the .NET libraries from the OSIsoft AF SDK
'''

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
