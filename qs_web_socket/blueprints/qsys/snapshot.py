"""

Examples
--------
{
    "command": "system",
    "payload": {
        "action": "load",
        "bank": 1
    }
}

"""

# pylint: disable=no-self-argument

from typing import Literal, Optional

from pydantic import BaseModel, ValidationError, field_validator

from ...drivers.qsc_core_qrc.client import QRCClient
from ...drivers.qsc_core_qrc.commands import Snapshot
from .id_generator import generate_id


class SnapshotPayload(BaseModel):
    action: Literal["load", "save"]
    bank: int
    name: str = "System_Controller"
    ramp: Optional[float] = 0.0

    @field_validator("ramp")
    def coerce_ramp(cls, v):
        return float(v) if v is not None else 0.0


async def snapshot_command(message: dict, client: QRCClient) -> tuple[bool, str]:
    try:
        payload = SnapshotPayload(**message.get("payload", {}))
    except ValidationError as e:
        messages = [err["msg"] for err in e.errors()]
        return False, "; ".join(messages)

    if payload.action == "load":
        cmd = Snapshot.Load(
            id_=generate_id(),
            name=payload.name,
            bank=payload.bank,
            ramp=payload.ramp,
        )
    else:
        cmd = Snapshot.Save(
            id_=generate_id(),
            name=payload.name,
            bank=payload.bank,
        )

    await client.send(*cmd)
    return True, f"successfully sent snapshot {payload.action} command"
