# pylint: disable=unused-import

import asyncio
import signal

from logging import getLogger
from websockets import serve

from .logging import configure_logging
from .drivers import DRIVERS

from .server.dispatcher import dispatcher

from .drivers.qsc_core_qrc.client import QRCClient

from .blueprints.qsys.routes import qsys_route_handler, handle_poll
from .blueprints.qsys.change_groups import register_change_group, invalidate_change_group

configure_logging()
logger = getLogger(__name__)


async def main():
    client = QRCClient("127.0.0.1", auto_reconnect=True)

    @client.on_connect
    async def __setup(client: QRCClient) -> None:
        await register_change_group(client)

    @client.on_change_group
    async def __handle_poll(payload: dict) -> None:
        await handle_poll(payload)

    @client.on_ws_client_connected
    async def __invalidate_group(client: QRCClient) -> None:
        await invalidate_change_group(client)

    client.initialize()
    client.connect()

    DRIVERS[QRCClient] = client
    stop_event = asyncio.Event()

    def handle_sigint(*_):
        logger.info("KeyboardInterrupt: shutting down...")
        stop_event.set()

    signal.signal(signal.SIGINT, handle_sigint)

    async with serve(
        dispatcher,
        "127.0.0.1",
        8765,
    ):
        logger.info("WebSocket server running on ws://0.0.0.0:8765")
        try:
            await stop_event.wait()
        finally:
            await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
