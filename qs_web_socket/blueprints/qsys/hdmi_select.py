"""

Examples
--------
{
    "command": "inputs",
    "payload": {
        "value": "input.1"
    }
}

"""
from functools import partial
from typing import Literal

from pydantic import BaseModel, ValidationError

from ...drivers.qsc_core_qrc.client import QRCClient
from ...drivers.qsc_core_qrc.commands import Component
from .id_generator import generate_id


class HDMIPayload(BaseModel):
    value: Literal["input.1", "input.2", "input.3"]

    def input_index(self) -> int:
        mapping = {
            "input.1": 1,
            "input.2": 2,
            "input.3": 3,
        }
        return mapping[self.value]


HDMI_SELECTOR = "Input_Controller"


async def hdmi_command(message: dict, client: QRCClient) -> tuple[bool, str]:
    try:
        payload = HDMIPayload(**message.get("payload", {}))
    except ValidationError as e:
        messages = [err["msg"] for err in e.errors()]
        return False, "; ".join(messages)

    base_command = partial(Component.Set, generate_id(), HDMI_SELECTOR)
    target_hdmi = f"hdmi.out.1.select.hdmi.{payload.input_index()}"

    cmd = base_command(
        [{"Name": target_hdmi, "Value": 1, "Ramp": 0}],
        response_values=True,
    )

    await client.send(*cmd)
    return True, f"successfully switched HDMI to {payload.value}"
