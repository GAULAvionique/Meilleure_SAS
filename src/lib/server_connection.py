"""
The module for the Telemetry-Server connection.
"""

from socket import socket, SHUT_RDWR, create_connection
from io import BufferedReader
from collections.abc import Callable

import logging
from threading import Thread, Event, Lock

# local imports
from .protocol import Data, decode


# Gets the logger
logger = logging.getLogger(__name__)
class ServerConnection:
    """
    Class for the client-server connection
    """

    addr: str
    port: int

    # the connection socket
    _sock: socket | None
    _sock_lock: Lock
    _reader: BufferedReader | None

    _stop_requested: Event

    # the callable to call when receiving data
    _on_samples: Callable[[list[Data]], None]

    _xgress_thread: Thread
    _reconnect_delay: float = 5.0

    @property
    def stop_requested(self) -> bool:
        """loops check this and stop if true"""
        return self._stop_requested.is_set()

    def __init__(self, addr: str, port: int, on_samples: Callable[[list[Data]], None]) -> None:
        self.addr = addr
        self.port = port
        self._on_samples = on_samples

        self._sock_lock = Lock()
        self._sock = None
        self._reader = None

        self._stop_requested = Event()

        self._xgress_thread = Thread(target=self._run, name="Socket-Thread")


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
            self._reader = sock.makefile("rb")



    def _read_sock(self):
        """
        reads the socket for incoming data
        """

        hello = self._reader.readline()
        logger.info("Hello received: %s", hello)

        while not self.stop_requested:
            data = self._reader.readline()

            # Checks if 'data' is empty, specifically b""
            # the readline method returns an empty bytes array when the client has disconnected
            if not data:

                # checks if the shutdown process was started
                # so it doesn't log on an intentional disconnect
                if not self.stop_requested:
                    logger.info("Server disconnected, trying to reconnect...")
                return


            # TODO make it do something when data isnt empty
            # in here comes the protocol.json parsing and stuff


    def stop(self):
        """
        Starts the stopping process by gently asking
        """
        # already blocked
        if self._stop_requested.is_set():
            return

        # if not already blocked
        self._stop_requested.set()
        self._unblock()

    def _unblock(self) -> None:
        """
        Unblocks and safely stops the threads
        """
        # grabs the lock
        with self._sock_lock:

            # checks if socket is not None
            if self._sock is not None:
                try:
                    # wakes the blocked readline with b""
                    self._sock.shutdown(SHUT_RDWR)
                except OSError:
                    pass

    def start(self):
        """
        Starts the threads
        """
        self._xgress_thread.start()

    def join(self) -> bool:
        """
        Joins the thread
        """

        self._xgress_thread.join(6.0)
        return not self._xgress_thread.is_alive()

    def _run(self) -> None:
        """
        Runs a single loop.
        """
        while not self.stop_requested:
            try:
                self._connect_to_server(self.addr, self.port)
            except OSError:
                # True if stop() was called meanwhile
                self._stop_requested.wait(self._reconnect_delay)
                continue

            # stop() landed mid-connect, before self._sock existed
            if self.stop_requested:
                self._close_sock()
                break

            try:
                # returns on EOF
                self._read_sock()
            except OSError as e:
                logger.warning("Connection lost: %s", e)
            finally:
                self._close_sock()

            self._stop_requested.wait(self._reconnect_delay)

    def _close_sock(self):
        with self._sock_lock:
            self._reader.close()
            self._sock.close()
            self._sock = None
            self._reader = None
