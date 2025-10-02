from typing import Any, Optional


class Control:
    @staticmethod
    def Get(id_: int, ctrl_names: str | list[str]) -> tuple[str, dict]:
        ctrl_params = [ctrl_names] if not isinstance(
            ctrl_names, list) else ctrl_names

        payload_params = {
            "id": id_,
            "params": ctrl_params
        }

        return "Control.Get", payload_params

    @staticmethod
    def Set(
        id_: int,
        ctrl_name: str,
        value: Any,
        ramp: Optional[float] = None
    ) -> tuple[str, dict]:
        ctrl_params = {"Name": ctrl_name, "Value": value}
        payload_params = {"id": id_, "params": ctrl_params}

        if ramp is not None:
            payload_params["params"]["Ramp"] = ramp

        return "Control.Set", payload_params
