from json import dumps
from websockets import ClientConnection

from ...server.router import ws_route
from ...server.dispatcher import CONNECTIONS
from ...drivers.qsc_core_qrc.client import QRCClient

from .lights import lights_command
from .snapshot import snapshot_command
from .hdmi_select import hdmi_command
from .dialer import dialer_command

COMMANDS = {
    "lights": lights_command,
    "system": snapshot_command,
    "inputs": hdmi_command,
    "dialer": dialer_command
}

COMPONENT_MAP = {
    "Input_Controller": {
        "frontend": "inputs",
        "controls": {
            "hdmi.out.1.select.hdmi.1": "input.1",
            "hdmi.out.1.select.hdmi.2": "input.2",
            "hdmi.out.1.select.hdmi.3": "input.3",
        },
    },
    "Shades_Controller": {
        "frontend": "shades",
        "controls": {
            "selector.0": "open",
            "selector.1": "close",
        },
    },
    "Lighting_Controller": {
        "frontend": "lights",
        "controls": {
            "selector.0": "lights.100",
            "selector.1": "lights.75",
            "selector.2": "lights.50",
            "selector.3": "lights.00",
        },
    },
    "System_Controller": {
        "frontend": "system",
        "controls": {
            "load.1": "preset.1",
            "load.2": "preset.2",
            "load.3": "preset.3",
            "load.4": "preset.4",
        },
    },
    "Dialer_Controller": {
        "frontend": "dialer",
        "controls": {
            "call.dnd": "dnd",
            "call.connect": "connect",
            "call.disconnect": "disconnect",
            "call.ringing": "ringing",
            "call.status": "status",
        },
    },
}


def _resolve_dialer(name: str, change: dict) -> str:
    value = change.get("Value", 0.0)
    string_val = change.get("String", "").strip().lower()

    if name == "call.dnd":
        return "on" if string_val == "on" or value != 0 else "off"

    if name == "call.ringing":
        return "ringing" if string_val == "true" or value != 0 else "idle"

    if name == "call.status":
        return change.get("String", "unknown")

    if name in ("call.connect", "call.disconnect"):
        return "enabled" if not change.get("Disabled", False) else "disabled"

    return str(value)


def _resolve_input_controller(change: dict) -> str:
    return "active" if change.get("Value", 0.0) != 0 else "inactive"


def _resolve_simple_on_off(change: dict) -> str:
    return "on" if change.get("Value", 0.0) != 0 else "off"


def _resolve_shades_controller(change: dict) -> str:
    return change.get("Value", 0.0) != 0


def _resolve_comp_status(change: dict, comp: str) -> str | bool:
    resolve_map = {
        "Input_Controller": _resolve_input_controller,
        "Lighting_Controller": _resolve_simple_on_off,
        "Shades_Controller": _resolve_shades_controller,
        "System_Controller": _resolve_simple_on_off
    }

    return resolve_map[comp](change)


async def handle_poll(params: dict):
    changes = params["Changes"]
    translated = translate_changes(changes)

    if translated:
        await notify_clients({
            "type": "change_group_update",
            "id": params["Id"],
            "components": translated,
        })


async def notify_clients(event: dict):
    message = dumps(event)
    connection_set: set[ClientConnection] = CONNECTIONS.get("/qsys", [])

    for ws in list(connection_set):
        try:
            await ws.send(message)
        except Exception:
            await ws.close()


@ws_route("/qsys")
async def qsys_route_handler(
    websocket: ClientConnection,
    message: dict,
    drivers: dict
):
    client: QRCClient = drivers.get(QRCClient)
    cmd = message.get("command", "").lower()
    qsys_command = COMMANDS.get(cmd)

    if not qsys_command:
        response = {"status": "error",
                    "message": f"unknown command: {cmd}"}
    else:
        success, msg = await qsys_command(message, client)
        response = {
            "status": "success" if success else "error",
            "command": cmd,
            "payload": {"message": msg}
        }

    await websocket.send(dumps(response))


def resolve_status(comp: str, name: str, change: dict) -> str:
    match comp:
        case "Input_Controller" | "Lighting_Controller" | "Shades_Controller" | "System_Controller":
            return _resolve_comp_status(change, comp)
        case "Dialer_Controller":
            return _resolve_dialer(name, change)
        case _:
            return str(change.get("Value", ""))


def translate_changes(changes: list[dict]) -> dict:
    result: dict[str, dict[str, str]] = {}

    for change in changes:
        comp = change["Component"]
        name = change["Name"]

        comp_map = COMPONENT_MAP.get(comp)

        if not comp_map:
            continue

        frontend_comp = comp_map["frontend"]
        frontend_name = comp_map["controls"].get(name, name)

        status = resolve_status(comp, name, change)

        if frontend_comp not in result:
            result[frontend_comp] = {}
        result[frontend_comp][frontend_name] = status

    return result
