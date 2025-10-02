"""

Examples
--------
{
    "command": "dialer",
    "payload": {
        "action": "dnd",
        "state": "enable"
    }
}

"""

# pylint: disable=no-self-argument

from functools import partial
from typing import Literal, Optional

from pydantic import BaseModel, ValidationError, field_validator, ValidationInfo

from ...drivers.qsc_core_qrc.client import QRCClient
from ...drivers.qsc_core_qrc.commands import Component
from .id_generator import generate_id


class DialerPayload(BaseModel):
    action: Literal["dial", "answer", "disconnect", "dnd"]
    digit: Optional[Literal["0", "1", "2", "3", "4",
                            "5", "6", "7", "8", "9", "*", "#"]] = None
    state: Optional[Literal["enable", "disable"]] = None

    @field_validator("digit", mode="before")
    def require_digit_if_dial(cls, v, info: ValidationInfo):
        if info.data.get("action") == "dial" and v is None:
            raise ValueError("digit is required when action='dial'")
        return v

    @field_validator("state", mode="before")
    def require_state_if_dnd(cls, v, info: ValidationInfo):
        if info.data.get("action") == "dnd" and v is None:
            raise ValueError("state is required when action='dnd'")
        return v


DIALER_SELECTOR = "Dialer_Controller"

PINPAD_MAPPING = {str(i): f"call.pinpad.{i}" for i in range(10)}
PINPAD_MAPPING.update({"*": "call.pinpad.*", "#": "call.pinpad.#"})

ACTION_MAPPING = {
    "answer": "call.connect",
    "disconnect": "call.disconnect",
}


async def dialer_command(message: dict, client: QRCClient) -> tuple[bool, str]:
    try:
        payload = DialerPayload(**message.get("payload", {}))
    except ValidationError as e:
        messages = [err["msg"] for err in e.errors()]
        return False, "; ".join(messages)

    base_command = partial(Component.Set, generate_id(), DIALER_SELECTOR)

    if payload.action == "dial":
        control_name = PINPAD_MAPPING[payload.digit]
        cmd = base_command(
            [{"Name": control_name, "Value": 1, "Ramp": 0}],
            response_values=True,
        )
        description = f"sent dialer digit {payload.digit}"

    elif payload.action == "dnd":
        value = 1 if payload.state == "enable" else 0
        cmd = base_command(
            [{"Name": "call.dnd", "Value": value, "Ramp": 0}],
            response_values=True,
        )
        description = f"DND {payload.state}d"

    else:
        control_name = ACTION_MAPPING[payload.action]
        cmd = base_command(
            [{"Name": control_name, "Value": 1, "Ramp": 0}],
            response_values=True,
        )
        description = f"{payload.action}ed call"

    await client.send(*cmd)
    return True, f"successfully {description}"
