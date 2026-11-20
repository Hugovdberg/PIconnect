import asyncio as py_asyncio
from typing import TYPE_CHECKING, TypeVar, TypeVarTuple, cast

_ParamTypes = TypeVarTuple("_ParamTypes")
_T = TypeVar("_T")

if TYPE_CHECKING:
    import System

    _TaskT = System.Threading.Tasks.Task
else:
    from .dotnet import System

    _TaskT = "System.Threading.Tasks.Task<T>"


def _set_future_result_on_completion(
    future: py_asyncio.Future[_T],
    loop: py_asyncio.AbstractEventLoop,
    task: "_TaskT[_T]",
) -> None:
    if task.IsFaulted:
        clr_error = cast(
            BaseException, cast(System.Exception, task.Exception).GetBaseException()
        )
        future.set_exception(clr_error)
    else:
        loop.call_soon_threadsafe(lambda: future.set_result(task.GetAwaiter().GetResult()))


def task_to_future(task: "_TaskT[_T]") -> py_asyncio.Future[_T]:
    """Create an asyncio.Future that is set when the clr_task is completed."""
    loop = py_asyncio.get_running_loop()
    future: py_asyncio.Future[_T] = loop.create_future()
    callback = System.Action(lambda: _set_future_result_on_completion(future, loop, task))  # type: ignore[ty:missing-argument]
    task.GetAwaiter().OnCompleted(callback)
    return future


class CancellationToken:
    """A simple wrapper around the .NET CancellationToken system."""

    def __init__(self) -> None:
        self._cancellation_token_source = System.Threading.CancellationTokenSource()
        self.token = self._cancellation_token_source.Token

    def cancel(self) -> None:
        self._cancellation_token_source.Cancel()


__all__ = ["task_to_future", "task_to_future", "CancellationToken"]
