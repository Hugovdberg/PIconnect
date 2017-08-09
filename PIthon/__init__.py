''' PIthon
    A python connector to the OSISoft PI and PI-AF databases

'''
import atexit
import pandas as pd

from AFSDK import AF
from PI import PIServer
from PIData import PISeries

piafServer = None
piafDB = None

def connectPIAFServer(server_name = '', database = ''):
    global piafServer
    global piafDB
    piServers = AF.PISystems()
    if server_name == '':
        piafServer = piServers.DefaultPISystem
    else:
        piafServer = piServers[server_name]
    piafServer.Connect()
    if database == '':
        piafDB = piafServer.Databases.DefaultDatabase
    else:
        piafDB = piafServer.Databases.get_Item(database)

def CurrentValue(tagname):
    # Check whether a single tag was passed or a list of tags
    if isinstance(tagname, list):
        currentvalues = [CurrentValue(tag) for tag in tagname]
        return pd.concat(currentvalues, axis = 1)
    elif not isinstance(tagname, basestring):
        raise TypeError('Argument tagname must be either a list or a string')

    # Determine whether a PI tag was passed or a PI-AF element
    if tagname.find('|') == -1:
        raise ValueError('')
    elif len(tagname.split('|')) == 2:
        return __CurrentValuePIAF(tagname)
    else:
        raise ValueError('Argument must be a PI-AF path of the form ElementPath|Attribute, '
                         'PI Points can be accessed through the PIServer class')

def __CurrentValuePIAF(elementpath):
    global piafDB
    if not piafDB:
        connectPIAFServer()

    element, attribute = elementpath.split('|')
    elem = piafDB.Elements.get_Item(element)
    attr = elem.Attributes.get_Item(attribute)
    lastData = attr.GetValue()
    return PISeries(elementpath,
                    [PISeries.timestamp_to_index(lastData.Timestamp.UtcTime)],
                    [lastData.Value],
                    lastData.UOM.Name)

def __disconnect():
    global piafServer
    if piafServer:
        piafServer.Disconnect()
        piafServer = None
atexit.register(__disconnect)
