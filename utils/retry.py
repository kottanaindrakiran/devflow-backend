import asyncio
import functools
from typing import Callable, Any
from .logger import logger

def async_retry(max_retries: int = 2, delay: float = 1.0):
    """
    Decorator to retry an async function upon failure.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {str(e)}")
                    if attempt < max_retries:
                        await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
            
            logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")
            raise last_exception
        return wrapper
    return decorator
