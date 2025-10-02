from typing import Optional

class Component:
    @staticmethod
    def Get(
        id_: int, component_name: str, ctrl_names: str | list[str]
    ) -> tuple[str, dict]:
        if isinstance(ctrl_names, str):
            ctrl_names = [ctrl_names]

        controls = [{"Name": name} for name in ctrl_names]

        payload_params = {
            "id": id_,
            "params": {
                "Name": component_name,
                "Controls": controls,
            },
        }

        return "Component.Get", payload_params

    @staticmethod
    def GetComponents(id_: int, params: Optional[str] = None) -> tuple[str, dict]:
        payload_params: dict = {"id": id_}

        if params is not None:
            payload_params["params"] = params

        return "Component.GetComponents", payload_params

    @staticmethod
    def GetControls(id_: int, component_name: str) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": component_name,
            },
        }

        return "Component.GetControls", payload_params

    @staticmethod
    def Set(
        id_: int,
        component_name: str,
        controls: list[dict],
        response_values: Optional[bool] = None
    ) -> tuple[str, dict]:
        payload_params: dict = {
            "id": id_,
            "params": {
                "Name": component_name,
                "Controls": controls,
            },
        }

        if response_values is not None:
            payload_params["params"]["ResponseValues"] = response_values

        return "Component.Set", payload_params
