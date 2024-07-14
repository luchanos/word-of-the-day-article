import asyncio
import logging
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)


def retry(n: int, delay: int = 0) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        async def inner(*args, **kwargs) -> Any:
            attempts = n
            while attempts > 0:
                try:
                    return await func(*args, **kwargs)
                except Exception as err:
                    attempts -= 1
                    if attempts == 0:
                        logger.error(f"All retries failed for {func.__name__}: {err}")
                        raise
                    else:
                        logger.warning(
                            f"Retrying {func.__name__} due to: {err}. {attempts} attempts left."
                        )
                        if delay > 0:
                            await asyncio.sleep(delay)

        return inner

    return wrapper
