from typing import Any, Awaitable, Callable

ROUTES: dict[str, Callable] = {}


def ws_route(path: str):
    def decorator(func: Callable[[Any, dict], Awaitable[None]]):
        ROUTES[path] = func
        return func
    return decorator
