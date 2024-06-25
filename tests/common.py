"""Common fixtures for testing PIconnect."""

import os

import pytest


def on_CI() -> bool:
    """Return True if the tests are running on a CI environment."""
    return (
        os.getenv("GITHUB_ACTIONS", "false").lower() == "true"
        or os.getenv("TF_BUILD", "false").lower() == "true"
        or os.getenv("READTHEDOCS", "false").lower() == "true"
    )


skip_if_on_CI = pytest.mark.skipif(on_CI(), reason="Real SDK not available on CI")
