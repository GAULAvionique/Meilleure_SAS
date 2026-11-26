"""
Error module
"""

class SASError(Exception):
    """
    Basic SAS error class for anything that can reasonably be handled
    """
    exit_code: 1

class ConfigError(SASError):
    """
    An error in config.
    """
    exit_code = 78

class StartupError(SASError):
    """
    An error happened while acquiring a resource or during the startup process at the OS level.
    """
    exit_code = 71

class InternalError(SASError):
    """
    Something happened but we really don't know what. Only a last resort for catching stuff in main.py
    This is because of a bug in the software of the SAS itself.
    """
    exit_code = 70
