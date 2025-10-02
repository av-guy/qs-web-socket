import asyncio

from typing import Callable, Optional, Any, Awaitable
from logging import getLogger

logger = getLogger(__name__)


class TCPConnection:
    def __init__(
        self,
        host_name: str,
        port: int,
        reconnect_delay: int = 5,
        auto_reconnect: bool = True,
        line_terminator: bytes = b'\r\n'
    ):
        self._host_name = host_name
        self._port = port
        self._reconnect_delay = reconnect_delay
        self._auto_reconnect = auto_reconnect

        self._writer: asyncio.StreamReader | None = None
        self._reader: asyncio.StreamReader | None = None

        self._connected = asyncio.Event()
        self._response_lock = asyncio.Lock()

        self._stopping = False
        self._line_terminator = line_terminator

        self._on_data_callbacks = []
        self._on_status_callbacks = []

    async def _emit_data(self, message: bytes):
        for cb in self._on_data_callbacks:
            try:
                await cb(message)
            except Exception as e:
                logger.warning("(%s:%s) on_data callback failed: %s",
                        self._host_name, self._port, e)

    async def _emit_status(self, connected: bool):
        for cb in self._on_status_callbacks:
            try:
                await cb(connected)
            except Exception as e:
                logger.warning("(%s:%s) on_status callback failed: %s",
                        self._host_name, self._port, e)

    async def _read_loop(self):
        buffer = b""

        try:
            while not self._reader.at_eof():
                async with self._response_lock:
                    chunk = await self._reader.read(1024)
                    if not chunk:
                        await asyncio.sleep(0.05)
                        continue

                    buffer += chunk
                    while self._line_terminator in buffer:
                        raw, buffer = buffer.split(self._line_terminator, 1)

                        if not raw:
                            continue

                        logger.debug("(%s:%s) Received message: %s",
                             self._host_name, self._port, raw)
                        await self._emit_data(raw)
        except (asyncio.CancelledError, ConnectionResetError) as e:
            logger.warning("(%s:%s) Read loop ended: %s",
                    self._host_name, self._port, e)
            raise ConnectionError(
                f"({self._host_name}:{self._port}) Server closed connection") from e

    async def connect(self):
        while not self._stopping:
            try:
                logger.info("Connecting to %s:%s...", self._host_name, self._port)
                self._reader, self._writer = await asyncio.open_connection(
                    self._host_name, self._port
                )

                self._connected.set()
                logger.info("Connected to %s:%s!", self._host_name, self._port)

                await self._emit_status(True)
                await self._read_loop()
            except (OSError, asyncio.IncompleteReadError, ConnectionError) as e:
                await self._emit_status(False)

                logger.warning("(%s:%s) Connection error: %s",
                        self._host_name, self._port, e)
                self._connected.clear()

                if not self._stopping and self._auto_reconnect:
                    logger.info("(%s:%s) Reconnecting in %s seconds...",
                         self._host_name, self._port, self._reconnect_delay)
                    await asyncio.sleep(self._reconnect_delay)

    async def disconnect(self):
        self._stopping = True
        self._connected.clear()

        if self._writer and isinstance(self._writer, asyncio.StreamWriter):
            self._writer.close()
            await self._writer.wait_closed()

        logger.info("(%s:%s) Disconnected", self._host_name, self._port)

    def on_data(
        self, func: Callable[[str], Awaitable[Any]]
    ) -> Callable[[str], Awaitable[Any]]:
        self._on_data_callbacks.append(func)
        return func

    def on_status(
        self, func: Callable[[str], Awaitable[Any]]
    ) -> Callable[[str], Awaitable[Any]]:
        self._on_status_callbacks.append(func)
        return func

    async def send(
        self,
        data: bytes | str,
        encoding: str = "utf-8",
        wait_for_response: bool = False,
        timeout: float = 5.0,
        line_terminator: Optional[bytes] = None
    ) -> Optional[bytes]:
        await self._connected.wait()

        if self._writer and isinstance(self._writer, asyncio.StreamWriter):
            if not isinstance(data, bytes):
                data = data.encode(encoding=encoding)

            if wait_for_response:
                async with self._response_lock:
                    self._writer.write(data)
                    await self._writer.drain()
                    logger.debug("(%s:%s) Sent: %s", self._host_name, self._port, data)

                    line_terminator = (
                        self._line_terminator if line_terminator
                        is None else line_terminator
                    )

                    buffer = b""
                    try:
                        while True:
                            chunk = await asyncio.wait_for(
                                self._reader.read(1024), timeout=timeout
                            )

                            if not chunk:
                                await asyncio.sleep(0.05)
                                continue

                            buffer += chunk

                            if line_terminator in buffer:
                                raw, buffer = buffer.split(
                                    self._line_terminator, 1)
                                if not raw:
                                    continue
                                return raw

                    except asyncio.TimeoutError:
                        logger.warning("(%s:%s) Response timed out for %s",
                                self._host_name, self._port, data)
                        return None
            else:
                self._writer.write(data)
                await self._writer.drain()
                logger.debug("(%s:%s) Sent: %s", self._host_name, self._port, data)

        return None
