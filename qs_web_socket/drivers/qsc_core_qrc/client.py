import asyncio

from json import dumps
from typing import Any, Callable, Awaitable
from logging import getLogger

from ...comms.tcp_client import TCPConnection

from .commands import Connection
from .responses import parse_response

SetupFn = Callable[["QRCClient"], Awaitable[None]]
ChangeGroupHandler = Callable[[dict], Awaitable[None]]
OnClientConnect = Callable[["QRCClient"], Awaitable[None]]

logger = getLogger(__name__)


class QRCClient:
    def __init__(
        self,
        host_name: str,
        auto_reconnect: bool = True,
        name: str = "QSYS Core 110f"
    ):
        self._host_name = host_name
        self._auto_reconnect = auto_reconnect
        self._name = name

        self._tcp_client = TCPConnection(
            self._host_name,
            1710,
            auto_reconnect=self._auto_reconnect,
            line_terminator=b"\x00"
        )

        self._heartbeat_task: asyncio.Task | None = None
        self._connect_task: asyncio.Task | None = None
        self._queue_worker_task: asyncio.Task | None = None
        self._queue: asyncio.Queue[bytes] = asyncio.Queue()

        self._setup_hooks: list[SetupFn] = []
        self._change_group_handlers: list[ChangeGroupHandler] = []
        self._client_connect_handlers: list[OnClientConnect] = []

        self._subscribed = False

    def _connection_changed(self, connected: bool):
        if connected:
            self._heartbeat_task = asyncio.create_task(self._send_heartbeat())
            if self._queue_worker_task is None:
                self._queue_worker_task = asyncio.create_task(
                    self._queue_worker())
            logger.info("(%s) Sending heartbeat", self._name)

            for hook in self._setup_hooks:
                asyncio.create_task(hook(self))
        else:
            if self._heartbeat_task is not None:
                self._heartbeat_task.cancel()
                self._heartbeat_task = None
                logger.info("(%s) Cancelling heartbeat", self._name)

            if self._queue_worker_task is not None:
                self._queue_worker_task.cancel()
                self._queue_worker_task = None

    def _format_message(self, method: str, params: dict[str, Any]) -> bytes:
        message = {"jsonrpc": "2.0", "method": method, **params}
        return dumps(message).encode("utf-8") + b"\x00"

    def _msg_received(self, data: bytes):
        status, payload = parse_response(data, self._name)

        if status is not None:
            if status == "result":
                logger.info("(%s) Result: %s",
                            self._name, payload)

                method = payload.get("method", "")

                if method == "ChangeGroup.Poll":
                    for handler in self._change_group_handlers:
                        asyncio.create_task(handler(payload["params"]))
            else:
                logger.error("(%s) logger.error: %s",
                             self._name, payload)

    async def _send_heartbeat(self):
        while True:
            if self._queue.empty():
                await self._queue.put(self._format_message(*Connection.NoOp()))
            await asyncio.sleep(15)

    async def _queue_worker(self):
        while True:
            message = await self._queue.get()
            try:
                await self._tcp_client.send(message)
            except Exception as e:
                logger.info("(%s) Failed to send message: %s", self._name, e)
            finally:
                self._queue.task_done()

    def connect(self):
        self._connect_task = asyncio.create_task(self._tcp_client.connect())

    async def disconnect(self):
        if self._connect_task is not None:
            self._connect_task.cancel()

        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None

        if self._queue_worker_task is not None:
            self._queue_worker_task.cancel()
            self._queue_worker_task = None

        await self._tcp_client.disconnect()

    def initialize(self):
        @self._tcp_client.on_data
        async def __on_data(data: bytes):
            self._msg_received(data)

        @self._tcp_client.on_status
        async def __on_status(connected: bool):
            self._connection_changed(connected)

    def on_connect(self, fn: SetupFn) -> SetupFn:
        self._setup_hooks.append(fn)
        return fn

    def on_change_group(self, fn: ChangeGroupHandler) -> ChangeGroupHandler:
        self._change_group_handlers.append(fn)
        return fn

    def on_ws_client_connected(self, fn):
        self._client_connect_handlers.append(fn)
        return fn

    async def ws_client_connected(self):
        for handler in self._client_connect_handlers:
            await handler(self)

    async def send(self, method: str, params: dict[str, Any]):
        message: bytes = self._format_message(method, params)
        await self._queue.put(message)
