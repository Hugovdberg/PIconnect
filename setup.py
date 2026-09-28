"""Setup script for the package."""

import setuptools
import versioneer

setuptools.setup(
    name="PIconnect",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
