import logging
import time
from functools import wraps

logger = logging.getLogger("retry")


def with_retry(max_attempts: int = 3, backoff_seconds: float = 1.0):
    """Decorator: retries a function on any exception, with linear backoff.

    Used for LLM/STT calls (SumoPod, Groq) which can transiently fail on a flaky
    network — not for calls whose failure is a real application error (e.g. a 400
    from bad input, which should just propagate immediately).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger.warning(
                        "%s failed (attempt %d/%d): %s", func.__name__, attempt, max_attempts, e
                    )
                    if attempt < max_attempts:
                        time.sleep(backoff_seconds * attempt)
            raise last_exc

        return wrapper

    return decorator
