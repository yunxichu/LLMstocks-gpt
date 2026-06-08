"""AKShare rate-limiting and retry helpers.

All AKShare-touching functions in this package should be decorated with
`@rate_limited` so we get:
  * a single global lock (serialized requests to EastMoney endpoints)
  * a minimum interval between calls (env: AKSHARE_REQUEST_INTERVAL, default 0.8s)
  * up to 3 retries with linear backoff on exceptions
"""

from __future__ import annotations

import logging
import os
import threading
import time
from functools import wraps
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])

_LOCK = threading.Lock()
_LAST_CALL_TS: list[float] = [0.0]
_INTERVAL = float(os.getenv("AKSHARE_REQUEST_INTERVAL", "0.8"))
_MAX_RETRIES = 3
_BASE_BACKOFF_SECS = 2.0


def rate_limited(fn: F) -> F:
    """Serialize calls, enforce minimum interval, retry up to 3 times."""

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        last_err: Exception | None = None
        for attempt in range(_MAX_RETRIES):
            with _LOCK:
                elapsed = time.time() - _LAST_CALL_TS[0]
                if elapsed < _INTERVAL:
                    time.sleep(_INTERVAL - elapsed)
                try:
                    result = fn(*args, **kwargs)
                    _LAST_CALL_TS[0] = time.time()
                    return result
                except Exception as e:  # noqa: BLE001
                    last_err = e
                    _LAST_CALL_TS[0] = time.time()
                    logger.warning(
                        "%s attempt %d/%d failed: %s",
                        fn.__name__,
                        attempt + 1,
                        _MAX_RETRIES,
                        e,
                    )
            time.sleep((attempt + 1) * _BASE_BACKOFF_SECS)
        assert last_err is not None
        raise last_err

    return wrapper  # type: ignore[return-value]
