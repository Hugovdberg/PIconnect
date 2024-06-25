"""Test the loading of the SDK connector."""

import os
import pathlib

import pytest

import PIconnect as PI


def on_CI() -> bool:
    """Return True if the tests are running on a CI environment."""
    return (
        os.getenv("GITHUB_ACTIONS", "false").lower() == "true"
        or os.getenv("TF_BUILD", "false").lower() == "true"
        or os.getenv("READTHEDOCS", "false").lower() == "true"
    )


# Skip this test module on CI as it requires the real SDK to be installed
pytestmark = pytest.mark.skipif(on_CI(), reason="Real SDK not available on CI")


def test_load_SDK_without_arguments_raises_no_exception() -> None:
    """Test that loading the SDK object without arguments raises no exception."""
    try:
        PI.get_PI_connector()
    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


def test_load_SDK_returns_PIconnect_object() -> None:
    """Test that loading the SDK object returns a PIConnector."""
    assert isinstance(PI.get_PI_connector(), PI.PIConnector)


def test_load_SDK_with_a_valid_path_returns_SDK_object() -> None:
    """Test that loading the SDK object with a path returns a PIConnector."""
    assembly_path = "c:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\"
    assert isinstance(PI.get_PI_connector(assembly_path), PI.PIConnector)


def test_load_SDK_with_a_valid_path_stores_path_in_connector() -> None:
    """Test that loading the SDK object with a path stores the path in the connector."""
    assembly_path = "c:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\"
    connector = PI.get_PI_connector(assembly_path)
    assert connector.assembly_path == pathlib.Path(assembly_path)


def test_load_SDK_with_an_invalid_path_raises_import_error() -> None:
    """Test that loading the SDK object with an invalid path raises an ImportError."""
    assembly_path = "c:\\invalid\\path\\"
    with pytest.raises(ImportError, match="PIAF SDK not found at .*"):
        PI.get_PI_connector(assembly_path)


def test_load_SDK_with_valid_path_has_SDK_reference() -> None:
    """Test that loading the SDK object with a valid path has a reference to the SDK."""
    assembly_path = "c:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\"
    connector = PI.get_PI_connector(assembly_path)
    assert connector.AF is not None
