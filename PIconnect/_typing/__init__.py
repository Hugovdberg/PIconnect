"""Type stubs for the AF SDK and dotnet libraries."""

from typing import Protocol

from . import AF, System


class AFType(Protocol):
    # Modules
    # Analysis = AF.Analysis
    Asset = AF.Asset  # type: ignore[misc]
    # Collective = AF.Collective
    Data = AF.Data  # type: ignore[misc]
    # Diagnostics = AF.Diagnostics
    EventFrame = AF.EventFrame  # type: ignore[misc]
    # Modeling = AF.Modeling
    # Notification = AF.Notification
    PI = AF.PI  # type: ignore[misc]
    Search = AF.Search  # type: ignore[misc]
    # Support = AF.Support
    Time = AF.Time  # type: ignore[misc]
    # UI = AF.UI
    UnitsOfMeasure = AF.UnitsOfMeasure  # type: ignore[misc]

    # Classes
    # AFActiveDirectoryProperties = AF.AFActiveDirectoryProperties
    AFCategory = AF.AFCategory  # type: ignore[misc]
    AFCategories = AF.AFCategories  # type: ignore[misc]
    # AFChangedEventArgs = AF.AFChangedEventArgs
    # AFCheckoutInfo = AF.AFCheckoutInfo
    # AFClientRegistration = AF.AFClientRegistration
    # AFCollection = AF.AFCollection
    # AFCollectionList = AF.AFCollectionList
    # AFConnectionInfo = AF.AFConnectionInfo
    # AFContact = AF.AFContact
    # AFCsvColumn = AF.AFCsvColumn
    # AFCsvColumns = AF.AFCsvColumns
    AFDatabase = AF.AFDatabase  # type: ignore[misc]
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
    PISystem = AF.PISystem  # type: ignore[misc]
    PISystems = AF.PISystems  # type: ignore[misc]
    # UniversalComparer = AF.UniversalComparer


class SystemType(Protocol):
    # Modules
    Data = System.Data  # type: ignore[misc]
    Net = System.Net  # type: ignore[misc]
    Security = System.Security  # type: ignore[misc]

    # Classes
    DateTime = System.DateTime  # type: ignore[misc]
    Exception = System.Exception  # type: ignore[misc]
    TimeSpan = System.TimeSpan  # type: ignore[misc]


AF_SDK_VERSION = "2.7_compatible"

__all__ = ["AF", "AF_SDK_VERSION", "AFType", "System"]
