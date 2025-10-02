from ...drivers.qsc_core_qrc.client import QRCClient
from ...drivers.qsc_core_qrc.commands import ChangeGroup
from .id_generator import generate_id

CHANGE_GROUP_ID = "Conference_Change_Group"

CHANGE_GROUP_COMPONENTS = [
    {
        "Name": "Input_Controller",
        "Controls": [
            "hdmi.out.1.select.hdmi.1",
            "hdmi.out.1.select.hdmi.2",
            "hdmi.out.1.select.hdmi.3",
        ],
    },
    {
        "Name": "Shades_Controller",
        "Controls": [
            "selector.0",
            "selector.1",
        ],
    },
    {
        "Name": "Lighting_Controller",
        "Controls": [
            "selector.0",
            "selector.1",
            "selector.2",
            "selector.3",
        ],
    },
    {
        "Name": "System_Controller",
        "Controls": [
            "load.1",
            "load.2",
            "load.3",
            "load.4",
        ],
    },
    {
        "Name": "Dialer_Controller",
        "Controls": [
            "call.dnd",
            "call.connect",
            "call.disconnect",
            "call.ringing",
            "call.status",
        ],
    },
]


async def invalidate_change_group(client: QRCClient) -> tuple[bool, str]:
    invalidate_group_cmd = ChangeGroup.Invalidate(
        generate_id(), CHANGE_GROUP_ID)

    await client.send(*invalidate_group_cmd)


async def register_change_group(client: QRCClient) -> tuple[bool, str]:
    for change_group in CHANGE_GROUP_COMPONENTS:
        change_group_cmd = ChangeGroup.AddComponentControl(
            generate_id(),
            CHANGE_GROUP_ID,
            change_group["Name"],
            change_group["Controls"]
        )
        await client.send(*change_group_cmd)

    change_group_auto_poll = ChangeGroup.AutoPoll(
        generate_id(), CHANGE_GROUP_ID, 3)

    await client.send(*change_group_auto_poll)
