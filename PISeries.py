from pandas import Series

class PISeries(Series):
    def __init__(self, tag, timestamp, value, uom = None, *args, **kwargs):
        Series.__init__(self, data = value, index = timestamp, name = tag, *args, **kwargs)
        self.tag = tag
        self.uom = uom
