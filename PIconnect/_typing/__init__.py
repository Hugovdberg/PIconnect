"""Type stubs for the AF SDK and dotnet libraries."""

from typing import Protocol

from . import AF
from . import dotnet as System


class AFType(Protocol):
    # Modules
    # Analysis = AF.Analysis
    Asset = AF.Asset
    # Collective = AF.Collective
    Data = AF.Data
    # Diagnostics = AF.Diagnostics
    EventFrame = AF.EventFrame
    # Modeling = AF.Modeling
    # Notification = AF.Notification
    PI = AF.PI
    # Search = AF.Search
    # Support = AF.Support
    Time = AF.Time
    # UI = AF.UI
    UnitsOfMeasure = AF.UnitsOfMeasure

    # Classes
    # AFActiveDirectoryProperties = AF.AFActiveDirectoryProperties
    AFCategory = AF.AFCategory
    AFCategories = AF.AFCategories
    # AFChangedEventArgs = AF.AFChangedEventArgs
    # AFCheckoutInfo = AF.AFCheckoutInfo
    # AFClientRegistration = AF.AFClientRegistration
    # AFCollection = AF.AFCollection
    # AFCollectionList = AF.AFCollectionList
    # AFConnectionInfo = AF.AFConnectionInfo
    # AFContact = AF.AFContact
    # AFCsvColumn = AF.AFCsvColumn
    # AFCsvColumns = AF.AFCsvColumns
    AFDatabase = AF.AFDatabase
    # AFDatabases = AF.AFDatabases
    # AFErrors = AF.AFErrors
    # AFEventArgs = AF.AFEventArgs
    # AFGlobalRestorer = AF.AFGlobalRestorer
    # AFGlobalSettings = AF.AFGlobalSettings
    # AFKeyedResults = AF.AFKeyedResults
    # AFLibraries = AF.AFLibraries
    # AFLibrary = AF.AFLibrary
    # AFListResults = AF.AFListResults
    # AFNamedCollection = AF.AFNamedCollection
    # AFNamedCollectionList = AF.AFNamedCollectionList
    # AFNameSubstitution = AF.AFNameSubstitution
    # AFObject = AF.AFObject
    # AFOidcIdentity = AF.AFOidcIdentity
    # AFPlugin = AF.AFPlugin
    # AFPlugins = AF.AFPlugins
    # AFProgressEventArgs = AF.AFProgressEventArgs
    # AFProvider = AF.AFProvider
    # AFRole = AF.AFRole
    # AFSDKExtension = AF.AFSDKExtension
    # AFSecurity = AF.AFSecurity
    # AFSecurityIdentities = AF.AFSecurityIdentities
    # AFSecurityIdentity = AF.AFSecurityIdentity
    # AFSecurityMapping = AF.AFSecurityMapping
    # AFSecurityMappings = AF.AFSecurityMappings
    # AFSecurityRightsExtension = AF.AFSecurityRightsExtension
    # NumericStringComparer = AF.NumericStringComparer
    PISystem = AF.PISystem
    PISystems = AF.PISystems
    # UniversalComparer = AF.UniversalComparer


class SystemType(Protocol):
    # Modules
    Data = System.Data
    Net = System.Net
    Security = System.Security

    # Classes
    DateTime = System.DateTime
    Exception = System.Exception
    TimeSpan = System.TimeSpan


AF_SDK_VERSION = "2.7_compatible"

__all__ = ["AF", "AF_SDK_VERSION", "AFType", "System"]
