"""

Examples
--------
{
    "command": "inputs",
    "payload": {
        "value": "lights.100"
    }
}

"""

from functools import partial
from typing import Literal

from pydantic import BaseModel, ValidationError

from ...drivers.qsc_core_qrc.client import QRCClient
from ...drivers.qsc_core_qrc.commands import Component
from .id_generator import generate_id


class LightsPayload(BaseModel):
    value: Literal["lights.100", "lights.75", "lights.50", "lights.00"]

    def selector_index(self) -> int:
        mapping = {
            "lights.100": 0,
            "lights.75": 1,
            "lights.50": 2,
            "lights.00": 3,
        }
        return mapping[self.value]


LIGHTS_SELECTOR = "Lighting_Controller"


async def lights_command(message: dict, client: QRCClient) -> tuple[bool, str]:
    try:
        payload = LightsPayload(**message.get("payload", {}))
    except ValidationError as e:
        messages = [err["msg"] for err in e.errors()]
        return False, "; ".join(messages)

    base_command = partial(Component.Set, generate_id(), LIGHTS_SELECTOR)
    cmd = base_command(
        [{"Name": f"selector.{payload.selector_index()}", "Value": 1, "Ramp": 0}],
        response_values=True,
    )

    await client.send(*cmd)
    return True, f"successfully sent lights {payload.value} command"
