from typing import Callable, Generic, Type, TypeVar

_T = TypeVar("_T")
_V = TypeVar("_V")


class classproperty(Generic[_T, _V]):
    # Copyright Denis Ryzhkov, https://stackoverflow.com/a/13624858/4398595

    def __init__(self, fget: Callable[[Type[_T]], _V]) -> None:
        self.fget = fget
        self.__doc__ = fget.__doc__

    def __get__(self, instance: _T, owner_cls: Type[_T]) -> _V:
        return self.fget(owner_cls)
