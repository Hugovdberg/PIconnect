import enum


class AFBoundaryType(enum.IntEnum):
    """Mock class of the AF.Data.AFBoundaryType enumeration"""

    Inside = 0
    Outside = 1
    Interpolated = 2
