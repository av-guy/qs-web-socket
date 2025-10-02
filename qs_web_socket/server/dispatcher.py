
from json import dumps, loads, JSONDecodeError
from logging import getLogger

from websockets import ClientConnection

from .router import ROUTES
from ..drivers import DRIVERS

CONNECTIONS: dict[str, set[ClientConnection]] = {}
logger = getLogger(__name__)


async def dispatcher(websocket: ClientConnection):
    path = websocket.request.path

    if path not in ROUTES:
        await websocket.send(dumps({"error": f"unknown path {path}"}))
        await websocket.close()
        return

    if path not in CONNECTIONS:
        CONNECTIONS[path] = set({})

    connection_set: set = CONNECTIONS[path]
    connection_set.add(websocket)

    handler = ROUTES[path]
    logger.info("WebSocket client connected on %s", path)

    for comm_driver in DRIVERS.values():
        await comm_driver.ws_client_connected()

    try:
        async for raw in websocket:
            logger.info("[%s] WS Received: %s", path, raw)
            try:
                message = loads(raw)
            except JSONDecodeError:
                await websocket.send(dumps({"error": "invalid json"}))
                continue

            await handler(websocket, message, DRIVERS)
    finally:
        logger.info("WebSocket client disconnected from %s", path)
        connection_set: set = CONNECTIONS[path]
        connection_set.remove(websocket)
