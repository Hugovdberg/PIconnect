import sys
import os.path
import datetime
import pytz
import atexit

import clr
import pandas as pd

piaf_sdk_32 = 'C:\\Program Files\\PIPC\\AF\\PublicAssemblies\\4.0\\'
piaf_sdk_64 = 'C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\'
if os.path.isdir(piaf_sdk_32):
    sys.path.append(piaf_sdk_32)
elif os.path.isdir(piaf_sdk_64):
    sys.path.append(piaf_sdk_64)
else:
    raise ImportError('PIAF SDK not found, check installation')

clr.AddReference('OSIsoft.AFSDK')
from OSIsoft import AF
from OSIsoft.AF import Analysis
from OSIsoft.AF import Asset
from OSIsoft.AF import Collective
from OSIsoft.AF import Data
from OSIsoft.AF import Diagnostics
from OSIsoft.AF import EventFrame
from OSIsoft.AF import Modeling
from OSIsoft.AF import Notification
from OSIsoft.AF import PI
from OSIsoft.AF import Search
from OSIsoft.AF import Time
from OSIsoft.AF import UI
from OSIsoft.AF import UnitsOfMeasure

from PISeries import PISeries

piServer = None
piafServer = None
piafDB = None


def connectPIServer(serverName = ''):
    global piServer
    piServers = PI.PIServers()
    if serverName == '':
        piServer = piServers.DefaultPIServer
    else:
        piServer = piServers[serverName]
    piServer.Connect(False)


def connectPIAFServer(serverName = '', database = ''):
    global piafServer
    global piafDB
    piServers = AF.PISystems()
    if serverName == '':
        piafServer = piServers.DefaultPISystem
    else:
        piafServer = piServers[serverName]
    piafServer.Connect()
    if database == '':
        piafDB = piafServer.Databases.DefaultDatabase
    else:
        piafDB = piafServer.Databases.get_Item(database)


def SearchTags(query, source = None):
    global piServer
    if not piServer:
        connectPIServer()
    tags = PI.PIPoint.FindPIPoints(piServer, query, source, None)
    return [tag.Name for tag in tags]


def CurrentValue(tagname):
    # Check whether a single tag was passed or a list of tags
    if isinstance(tagname, list):
        currentvalues = list()
        for tag in tagname:
            currentvalues.append(CurrentValue(tag))
        return pd.concat(currentvalues, axis = 1)
    elif not isinstance(tagname, basestring):
        raise TypeError('Argument tagname must be either a list or a string')

    # Determine whether a PI tag was passed or a PI-AF element
    if tagname.find('|') == -1:
        return __CurrentValuePI(tagname)
    elif len(tagname.split('|')) == 2:
        return __CurrentValuePIAF(tagname)
    else:
        raise ValueError('Argument must be either a PI-tag'
            ' or a PI-AF path of the form ElementPath|Attribute')


def __CurrentValuePI(tagname):
    global piServer
    if not piServer:
        connectPIServer()
    tag = PI.PIPoint.FindPIPoint(piServer, tagname)
    lastData = tag.Snapshot()
    return PISeries(tagname,
                    [__timestamp_to_index(lastData.Timestamp.UtcTime)],
                    [lastData.Value])


def __CurrentValuePIAF(elementpath):
    global piafDB
    if not piafDB:
        connectPIAFServer()

    element, attribute = elementpath.split('|')
    elem = piafDB.Elements.get_Item(element)
    attr = elem.Attributes.get_Item(attribute)
    lastData = attr.GetValue()
    return PISeries(elementpath,
                    [__timestamp_to_index(lastData.Timestamp.UtcTime)],
                    [lastData.Value],
                    lastData.UOM.Name)


def CompressedData(tagname, starttime, endtime):
    global piServer
    if not piServer:
        connectPIServer()
    timeRange = Time.AFTimeRange(starttime, endtime)
    tag = PI.PIPoint.FindPIPoint(piServer, tagname)
    pivalues = tag.RecordedValues(timeRange,
                                  Data.AFBoundaryType.Inside,
                                  None,
                                  None)
    return pd.DataFrame([__value_to_dict(x.Value, x.Timestamp.UtcTime)
                         for x in pivalues])


def SampledData(tagname, starttime, endtime, interval):
    global piServer
    if not piServer:
        connectPIServer()
    timeRange = Time.AFTimeRange(starttime, endtime)
    span = Time.AFTimeSpan.Parse(interval)
    tag = PI.PIPoint.FindPIPoint(piServer, tagname)
    pivalues = tag.InterpolatedValues(timeRange, span, "", False)
    return pd.DataFrame([__value_to_dict(x.Value, x.Timestamp.UtcTime)
                         for x in pivalues])


def __timestamp_to_index(timestamp):
    local_tz = pytz.timezone('Europe/Amsterdam')
    return datetime.datetime(
        timestamp.Year,
        timestamp.Month,
        timestamp.Day,
        timestamp.Hour,
        timestamp.Minute,
        timestamp.Second,
        timestamp.Millisecond*1000
        ).replace(tzinfo = pytz.utc).astimezone(local_tz)


def __value_to_dict(value, timestamp):
    local_tz = pytz.timezone('Europe/Amsterdam')
    return {
        'Value': value,
        'Timestamp': datetime.datetime(
            timestamp.Year,
            timestamp.Month,
            timestamp.Day,
            timestamp.Hour,
            timestamp.Minute,
            timestamp.Second,
            timestamp.Millisecond*1000
            ).replace(tzinfo = pytz.utc).astimezone(local_tz)
    }


def __disconnect():
    global piServer
    global piafServer
    if piServer:
        piServer.Disconnect()
        piServer = None
    if piafServer:
        piafServer.Disconnect()
        piafServer = None
atexit.register(__disconnect)
