from datetime import datetime
from pydantic import BaseModel
from typing import *

from level import Level


class Logger(BaseModel):
    """
    A configurable logging class that provides colored console output for different logging levels.

    This class extends Pydantic's BaseModel to provide data validation and implements
    standard logging functionality with colored output for different severity levels.

    Attributes:
        level (Level): The minimum logging level for this logger instance
        name (str): The name identifier for this logger instance
    """

    class Config:
        """Pydantic configuration to allow arbitrary types."""

        arbitrary_types_allowed = True

    level: Level
    name: str

    @classmethod
    def get_logger(
        cls,
        name: str,
        level: Level = Level.INFO,
    ) -> "Logger":
        """
        Factory method to create a new Logger instance.

        Args:
            name (str): The name identifier for the logger
            level (Level, optional): The minimum logging level. Defaults to Level.INFO

        Returns:
            Logger: A new Logger instance with the specified name and level
        """
        logger: "Logger" = Logger(
            level=level,
            name=name,
        )

        logger.info(message=f"Initialized Logger '{logger.name}'...")

        return logger

    def _colourise_(
        self,
        level: Level,
        message: str,
    ) -> str:
        """
        Internal method to add ANSI color codes to log messages based on their level.

        Args:
            level (Level): The logging level determining the color
            message (str): The message to be colorized

        Returns:
            str: The colorized message with ANSI escape codes
        """
        colourisation: Dict[str, Any] = {
            "RESET": "\x1b[0m",
            "DEBUG": "\x1b[90m",  # Gray
            "INFO": "\x1b[94m",  # Blue
            "WARNING": "\x1b[93m",  # Yellow
            "ERROR": "\x1b[91m",  # Red
            "CRITICAL": "\x1b[91m",  # Red
        }

        return f"{colourisation[level.value]}{message}{colourisation['RESET']}"

    def critical(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Log a critical message.

        Args:
            message (str): The critical message to log
            **kwargs: Additional keyword arguments passed to log()
        """
        self.log(
            message,
            level=Level.CRITICAL,
            **kwargs,
        )

    def debug(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Log a debug message.

        Args:
            message (str): The debug message to log
            **kwargs: Additional keyword arguments passed to log()
        """
        self.log(
            message,
            level=Level.DEBUG,
            **kwargs,
        )

    def error(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Log an error message.

        Args:
            message (str): The error message to log
            **kwargs: Additional keyword arguments passed to log()
        """
        self.log(
            message,
            level=Level.ERROR,
            **kwargs,
        )

    def function(
        self,
        function: Callable[..., Any],
        *args,
        **kwargs,
    ) -> Any:
        """
        Decorator to log the execution of a function.

        Args:
            function (Callable[..., Any]): The function to be decorated
            *args: Positional arguments passed to the function
            **kwargs: Keyword arguments passed to the function

        Returns:
            Any: The result of the decorated function
        
        Raises:
            Exception: If an exception occurs during function execution
        """
        result: Any | None = None

        self.log(
            f"Executing: {function.__name__}",
            level=Level.INFO,
        )

        start: datetime = datetime.now()

        try:
            result = function(*args, **kwargs)

            self.log(
                f"Completed: {function.__name__}",
                level=Level.INFO,
            )
        except Exception as e:
            self.error(
                message=f"Caught an exception while attempting to execute function '{function.__name__}': {e}"
            )

        end: datetime = datetime.now()

        self.log(
            f"Duration: {(end - start).total_seconds()}s",
            level=Level.INFO,
        )

        return result

    def info(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Log an informational message.

        Args:
            message (str): The info message to log
            **kwargs: Additional keyword arguments passed to log()
        """
        self.log(
            message,
            level=Level.INFO,
            **kwargs,
        )

    def log(
        self,
        message: str,
        level: Level = Level.INFO,
        **kwargs,
    ) -> None:
        """
        Core logging method that handles message formatting and output.

        Args:
            message (str): The log message to output
            level (Level, optional): The severity level of the message. Defaults to Level.INFO
            **kwargs: Additional keyword arguments for future extensibility
        """
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{self.name}] {self._colourise_(level, message)}",
        )

    def warning(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Log a warning message.

        Args:
            message (str): The warning message to log
            **kwargs: Additional keyword arguments passed to log()
        """
        self.log(
            message,
            level=Level.WARNING,
            **kwargs,
        )
