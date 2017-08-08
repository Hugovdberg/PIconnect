import sys
import datetime

import clr
import pandas as pd

sys.path.append('C:\\Program Files\\PIPC\\AF\\PublicAssemblies\\4.0\\')

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


def connect_to_PIserver(serverName):
    piServers = PI.PIServers()
    global piServer
    piServer = piServers[serverName]
    piServer.Connect(False)

def connect_to_PIAFserver(serverName):
    piServers = AF.PISystems()
    global piafServer
    global piafDB
    piafServer = piServers[serverName]
    piafServer.Connect()
    piafDB = piafServer.Databases.DefaultDatabase

def get_tag_snapshot(tagname):
    tag = PI.PIPoint.FindPIPoint(piServer, tagname)
    lastData = tag.Snapshot()
    return lastData.Value, lastData.Timestamp

def get_tag_values(tagname, starttime, endtime):
    timeRange = Time.AFTimeRange(starttime, endtime)
    tag = PI.PIPoint.FindPIPoint(piServer, tagname)
    pivalues = tag.RecordedValues(timeRange, 0, None, None)
    df = pd.DataFrame([{'Value': x.Value, 'Timestamp': x.Timestamp.LocalTime} for x in pivalues])
    df.Timestamp = df.Timestamp.apply(lambda x: datetime.datetime(x.Year, x.Month, x.Day, x.Hour, x.Minute, x.Second, x.Millisecond*1000), convert_dtype = True)
    return df
