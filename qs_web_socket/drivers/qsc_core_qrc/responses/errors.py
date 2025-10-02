from enum import IntEnum


class QRCErrorCode(IntEnum):
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    SERVER_ERROR = -32603
    CORE_STANDBY = -32604

    INVALID_PAGE_REQUEST_ID = 2
    BAD_PAGE_REQUEST = 3
    MISSING_FILE = 4
    CHANGE_GROUPS_EXHAUSTED = 5
    UNKNOWN_CHANGE_GROUP = 6
    UNKNOWN_COMPONENT = 7
    UNKNOWN_CONTROL = 8
    ILLEGAL_MIXER_CHANNEL = 9
    LOGON_REQUIRED = 10

    @property
    def description(self) -> str:
        return {
            QRCErrorCode.PARSE_ERROR: "Parse error. Invalid JSON was received by the server.",
            QRCErrorCode.INVALID_REQUEST: "Invalid request. The JSON sent is not a valid Request object.",
            QRCErrorCode.METHOD_NOT_FOUND: "Method not found.",
            QRCErrorCode.INVALID_PARAMS: "Invalid params.",
            QRCErrorCode.SERVER_ERROR: "Server error.",
            QRCErrorCode.CORE_STANDBY: "Core is on Standby (not active in redundant configuration).",
            QRCErrorCode.INVALID_PAGE_REQUEST_ID: "Invalid Page Request ID.",
            QRCErrorCode.BAD_PAGE_REQUEST: "Bad Page Request - could not create the requested Page Request.",
            QRCErrorCode.MISSING_FILE: "Missing file.",
            QRCErrorCode.CHANGE_GROUPS_EXHAUSTED: "Change Groups exhausted.",
            QRCErrorCode.UNKNOWN_CHANGE_GROUP: "Unknown change group.",
            QRCErrorCode.UNKNOWN_COMPONENT: "Unknown component name.",
            QRCErrorCode.UNKNOWN_CONTROL: "Unknown control.",
            QRCErrorCode.ILLEGAL_MIXER_CHANNEL: "Illegal mixer channel index.",
            QRCErrorCode.LOGON_REQUIRED: "Logon required.",
        }[self]
