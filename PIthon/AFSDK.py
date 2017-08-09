''' AFSDK
	Loads the .NET libraries from the OSIsoft AF SDK
'''

import clr
import sys
import os

# Get the installation directory from the environment variable or fall back to the Windows
# default installation path
piaf_sdk = os.getenv('PIHOME', 'C:\\Program Files\\PIPC')
piaf_sdk += '\\AF\\PublicAssemblies\\4.0\\'
if not os.path.isdir(piaf_sdk):
    raise ImportError('PIAF SDK not found in %s, check installation' % piaf_sdk)

sys.path.append(piaf_sdk)
clr.AddReference('OSIsoft.AFSDK')

from OSIsoft import AF
