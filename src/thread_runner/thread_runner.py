import asyncio

from typing import *

from datetime import datetime

from queue import Queue

from threading import *

from logger import Logger


class ThreadRunner:
    """
    ThreadRunner is a utility class that provides methods to run functions concurrently
    within separate threads. It handles both running functions in existing threads
    and creating new ones as needed.

    Attributes:
        logger (Logger): A logger instance for logging messages related to thread execution.
    """

    logger: Logger = Logger.get_logger(name="ThreadRunner")

    @classmethod
    def _run_function_in_thread(
        cls,
        function: Callable[..., Any],
        result_queue: Queue,
        *args,
        **kwargs,
    ) -> None:
        """
        Helper method to run a single function in a new thread and collect the result.

        This method runs the given function in a new thread with the provided arguments
        and keyword arguments. It collects the result of the function and puts it into
        the result_queue. If an exception occurs while executing the function, it will
        be caught and put into the result_queue.

        The function is checked to determine if it is an asynchronous function. If it
        is, it is run inside an event loop to ensure that it is executed correctly.

        Args:
            function (Callable[..., Any]): The function to be executed in a thread.
            result_queue (Queue): A thread-safe queue to collect the result of the function.
            *args: Arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        """
        try:
            # Check if the function is an asynchronous function
            if asyncio.iscoroutinefunction(func=function):
                # If it is async, run it inside an event loop
                loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

                asyncio.set_event_loop(
                    loop=loop
                )  # Set the new event loop for this thread

                result: Any = loop.run_until_complete(
                    future=function(
                        *args,
                        **kwargs,
                    )
                )
            else:
                # If it's a regular synchronous function, run it directly
                result: Any = function(
                    *args,
                    **kwargs,
                )

            result_queue.put(result)  # Put the result into the queue
        except Exception as e:
            cls.logger.error(
                message=f"Caught an exception while attempting to run function in thread: {e}"
            )
            result_queue.put(e)  # Put the exception into the queue

    @classmethod
    def run_function(
        cls,
        function: Callable[..., Any],
        *args,
        **kwargs,
    ) -> Any:
        """
        Run the specified function using a new thread and return its result.

        This method creates a new thread to execute the given function and collects its result.
        If an exception occurs while executing the function, it will be caught and reraised.

        Args:
            function (Callable[..., Any]): The function object to be executed.
            *args: Arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            Any: The result returned by the function once it completes.

        Raises:
            Exception: Reraise any exception that occurs while executing the function.
        """
        try:
            # Record the start time
            start: datetime = datetime.now()

            # Log starting the thread
            cls.logger.info(message="Starting function execution in a new thread.")

            # Create a queue to collect the result
            result_queue: Queue = Queue()

            # Create and start the thread
            thread: Thread = Thread(
                target=cls._run_function_in_thread,
                args=(function, result_queue, *args),
                kwargs=kwargs,
            )

            # Start the thread
            thread.start()

            # Wait for the thread to finish
            thread.join()

            # Get the result from the queue
            result: Any = result_queue.get()

            # If the result is an exception, raise it
            if isinstance(result, Exception):
                raise result

            # Record the end time
            end: datetime = datetime.now()

            # Log finishing the thread
            cls.logger.info(
                message=f"Finished function execution in thread ({(end - start).total_seconds()}s)."
            )

            # Return the result
            return result

        except Exception as e:
            # Log any exceptions that occur while attempting to run the function in a new thread
            cls.logger.error(
                message=f"Caught an exception while attempting to run the function in a new thread: {e}"
            )

    @classmethod
    def run_functions(
        cls,
        functions: List[Callable[..., Any]],
        *args,
        **kwargs,
    ) -> List[Any]:
        """
        Run multiple functions concurrently in separate threads and return their results.

        Args:
            functions (List[Callable[..., Any]]): A list of function objects to be executed.
            *args: Arguments to pass to each function.
            **kwargs: Keyword arguments to pass to each function.

        Returns:
            List[Any]: A list of results returned by the functions once they complete.

        Raises:
            Exception: Reraise any exception that occurs while executing the functions.
        """
        try:
            # Record the start time
            start: datetime = datetime.now()

            # Log starting the threads
            cls.logger.info(message="Starting multiple function executions in threads.")

            # List to keep track of all created threads
            threads: List[Thread] = []

            # Queue to collect results from each thread
            result_queue: Queue = Queue()

            # List to store final results
            results: List[Any] = []

            # Create and start a thread for each function
            for function in functions:
                thread: Thread = Thread(
                    target=cls._run_function_in_thread,
                    args=(function, result_queue, *args),
                    kwargs=kwargs,
                )

                # Add the thread to the list of created threads
                threads.append(thread)

                # Start the thread
                thread.start()

            # Wait for all threads to finish execution
            for thread in threads:
                thread.join()

            # Collect results from the queue
            while not result_queue.empty():
                result: Any = result_queue.get()

                # If the result is an exception, raise it
                if isinstance(
                    result,
                    Exception,
                ):
                    raise result

                results.append(result)

            # Record the end time
            end: datetime = datetime.now()

            # Log finishing the thread
            cls.logger.info(
                message=f"Finished multiple function executions in threads ({(end - start).total_seconds()}s)."
            )

            # Return the results
            return results

        except Exception as e:
            # Log any exceptions that occur while attempting to run the functions in new threads
            cls.logger.error(
                message=f"Caught an exception while attempting to run the functions in new threads: {e}"
            )
