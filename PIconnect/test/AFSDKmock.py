import enum


class AF:
    class Data:
        class AFBoundaryType(enum.IntEnum):
            Inside = 0
            Outside = 1
            Interpolated = 2
    pass
