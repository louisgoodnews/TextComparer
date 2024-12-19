from enum import Enum


class Level(Enum):
    """
    Enumeration class representing different logging levels.
    
    This class defines standard logging levels used to categorize log messages
    based on their severity and importance.
    
    Levels in ascending order of severity:
        DEBUG: Detailed information for debugging purposes
        INFO: General information about program execution
        WARNING: Indicate a potential problem that doesn't prevent normal execution
        ERROR: Serious problem that prevents normal execution of a specific operation
        CRITICAL: Critical error that may prevent the entire application from running
    """
    
    # Used for detailed debugging information
    DEBUG = "DEBUG"
    
    # Used for general information messages
    INFO = "INFO"
    
    # Used for potentially harmful situations
    WARNING = "WARNING"
    
    # Used for error events that might still allow the application to continue running
    ERROR = "ERROR"
    
    # Used for very severe error events that will presumably lead to application failure
    CRITICAL = "CRITICAL"
