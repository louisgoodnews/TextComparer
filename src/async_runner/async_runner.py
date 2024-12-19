import asyncio
from typing import *
from pydantic import BaseModel
from logger import Logger


class AsyncRunner(BaseModel):
    """
    A class for managing and executing asynchronous coroutines.

    This class provides functionality to run single or multiple coroutines either in
    an existing event loop or in a new one. It implements the singleton pattern to
    ensure only one instance manages all async operations.

    Attributes:
        logger (Logger): Logger instance for the class
        loop (asyncio.AbstractEventLoop | None): The event loop being used
    """
    class Config:
        arbitrary_types_allowed = True

    # Initialize the class-level logger
    _logger: ClassVar[Logger] = Logger.get_logger(name="AsyncRunner")
    loop: Optional[asyncio.AbstractEventLoop] = None

    @classmethod
    async def _run_coroutine_in_loop_(cls, coroutine: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any | None:
        """Internal method to execute a coroutine with error handling.

        Args:
            coroutine (Callable[..., Awaitable[Any]]): The coroutine function to execute
            *args: Variable positional arguments to pass to the coroutine
            **kwargs: Variable keyword arguments to pass to the coroutine

        Returns:
            Any | None: The result of the coroutine execution, or None if an error occurred
        """
        try:
            return await coroutine(*args, **kwargs)
        except Exception as e:
            cls._logger.error(message=f"Caught an exception while attempting to run coroutine: {e}")
            return None

    @classmethod
    def run_coroutine(cls, coroutine: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any | None:
        """Execute a single coroutine.

        Attempts to run the coroutine in an existing event loop if available,
        otherwise creates a new one.

        Args:
            coroutine (Callable[..., Awaitable[Any]]): The coroutine function to execute
            *args: Variable positional arguments to pass to the coroutine
            **kwargs: Variable keyword arguments to pass to the coroutine

        Returns:
            Any | None: The result of the coroutine execution, or None if an error occurred
        """
        try:
            result: Any = None

            try:
                current_loop: Optional[asyncio.AbstractEventLoop] = (
                    asyncio.get_event_loop()
                )
                cls._logger.info(message="Found running event loop for coroutine.")
            except RuntimeError:
                cls._logger.warning(message="Found no running event loop for coroutine.")
                current_loop = None
            
            if current_loop and current_loop.is_running():
                cls._logger.info(message="Running coroutine in the existing event loop.")
                result = asyncio.create_task(
                    coroutine(*args, **kwargs)
                )
            else:
                cls._logger.info(message="Running coroutine in a new event loop.")
                result = asyncio.run(coroutine(*args, **kwargs))

            cls._logger.info(message="Finished running coroutine.")

            return result
        except Exception as e:
            cls._logger.error(message=f"Caught an exception while attempting to run coroutine: {e}")
            return None

    @classmethod
    def run_coroutines(cls, coroutines: List[Callable[..., Awaitable[Any]]], *args, **kwargs) -> List[Any] | None:
        """Execute multiple coroutines concurrently.

        Runs multiple coroutines either in an existing event loop or creates a new one.
        All coroutines are executed concurrently using asyncio.gather.

        Args:
            coroutines (List[Callable[..., Awaitable[Any]]]): List of coroutine functions to execute
            *args: Variable positional arguments to pass to each coroutine
            **kwargs: Variable keyword arguments to pass to each coroutine

        Returns:
            List[Any] | None: List of results from all coroutines, or None if an error occurred
        """
        try:
            results: List[Any] = []

            current_loop: asyncio.AbstractEventLoop | None

            try:
                current_loop = (
                    asyncio.get_event_loop()
                )

                cls._logger.info(message="Found running event loop for coroutines.")
            except RuntimeError:
                cls._logger.warning(
                    message="Found no running event loop for coroutines."
                )

                current_loop = None

            if current_loop and current_loop.is_running():
                cls._logger.info(
                    message="Running coroutines in the existing event loop."
                )
                results = current_loop.run_until_complete(
                    asyncio.gather(
                        *[
                            cls._run_coroutine_in_loop_(coroutine, *args, **kwargs)
                            for coroutine in coroutines
                        ]
                    )
                )
            else:
                cls._logger.info(message="Running coroutines in a new event loop.")

                results = asyncio.run(
                    asyncio.gather(
                        *[
                            cls._run_coroutine_in_loop_(coroutine, *args, **kwargs)
                            for coroutine in coroutines
                        ]
                    )
                )

            cls._logger.info(message="Finished running coroutines.")

            return results
        except Exception as e:
            cls._logger.error(message=f"Caught an exception while attempting to run coroutine: {e}")
            return None
