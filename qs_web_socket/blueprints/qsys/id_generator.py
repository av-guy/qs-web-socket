import itertools
import threading

_id_counter = itertools.count(1)
_lock = threading.Lock()


def generate_id() -> int:
    with _lock:
        return next(_id_counter)
