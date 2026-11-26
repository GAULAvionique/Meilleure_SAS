"""
The module for the Telemetry-Server connection.
"""

from socket import socket, AF_INET, SOL_SOCKET, SOCK_STREAM, SO_REUSEADDR, SHUT_RDWR, create_connection
from collections.abc import Callable

import logging
from threading import Lock

# local imports
from .protocol import Data


# Gets the logger
logger = logging.getLogger(__name__)
class ServerConnection:
    """
    Class for the client-server connection
    """

    # the connection socket
    _sock: socket
    _sock_lock: Lock

    # the callable to call when receiving data
    _on_samples: Callable[[list[Data]], None]

    def __init__(self, addr: str, port: int, on_samples: Callable[[list[Data]], None]) -> None:
        self._on_samples = on_samples

        self._sock_lock = Lock()

        self._connect_to_server(addr, port)

    def _connect_to_server(self, ip: str, port: int) -> None:

        # not 100% guaranteed to work, hence the catch
        try:
            sock = create_connection(address=(ip, port), timeout=5.0)
        except OSError as e:
            logger.info("Could not connect to %s:%s due to %s", ip, port, e)
            raise

        sock.settimeout(None)
        with self._sock_lock:
            self._sock = sock

        stuff = self._sock.makefile("rb").readline()
        logger.info("Got this: %s", stuff)
