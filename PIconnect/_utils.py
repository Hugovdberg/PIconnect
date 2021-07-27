class classproperty(object):
    # Copyright Denis Ryzhkov, https://stackoverflow.com/a/13624858/4398595
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
