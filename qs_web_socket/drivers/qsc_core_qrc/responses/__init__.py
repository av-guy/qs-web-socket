from logging import error
from json import loads, JSONDecodeError
from .errors import QRCErrorCode


def parse_response(message: bytes, name: str) -> tuple[None, None] | tuple[str, dict]:
    message = message.decode("utf-8")

    try:
        message = loads(message)
    except JSONDecodeError as e:
        error("(%s) Error decoding JSON: %s", name, e)
        return None, None

    if isinstance(message, dict):
        if "error" in message:
            err: dict = message["error"]

            code = err.get("code")
            msg = err.get("message", "Unknown error")

            try:
                enum_code = QRCErrorCode(code)
                error(
                    "(%s) JSON-RPC Error [%s]: %s",
                    name,
                    enum_code.name,
                    enum_code.description,
                )
            except ValueError:
                error("(%s) JSON-RPC Error [code=%s]: %s", name, code, msg)
            return "error", err

        if "result" in message:
            return "result", {
                "id": message.get("id"),
                "method": message.get("method"),
                "result": message["result"],
            }

        if "params" in message:
            return "result", {
                "id": message.get("id"),
                "method": message.get("method"),
                "params": message["params"],
            }

    return None, None
