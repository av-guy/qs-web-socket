class ChangeGroup:
    @staticmethod
    def AddControl(
        id_: int,
        group_id: str,
        controls: str | list[str],
    ) -> tuple[str, dict]:
        if isinstance(controls, str):
            controls = [controls]

        payload_params = {
            "id": id_,
            "params": {
                "Id": group_id,
                "Controls": controls,
            },
        }

        return "ChangeGroup.AddControl", payload_params

    @staticmethod
    def AddComponentControl(
        id_: int,
        group_id: str,
        component_name: str,
        controls: str | list[str],
    ) -> tuple[str, dict]:
        if isinstance(controls, str):
            controls = [controls]

        component = {
            "Name": component_name,
            "Controls": [{"Name": c} for c in controls],
        }

        payload_params = {
            "id": id_,
            "params": {
                "Id": group_id,
                "Component": component,
            },
        }

        return "ChangeGroup.AddComponentControl", payload_params

    @staticmethod
    def AutoPoll(
        id_: int,
        group_id: str,
        rate: int,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Id": group_id,
                "Rate": rate,
            },
        }

        return "ChangeGroup.AutoPoll", payload_params

    @staticmethod
    def Clear(
        id_: int,
        group_id: str,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Id": group_id,
            },
        }

        return "ChangeGroup.Clear", payload_params

    @staticmethod
    def Destroy(
        id_: int,
        group_id: str,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Id": group_id,
            },
        }

        return "ChangeGroup.Destroy", payload_params

    @staticmethod
    def Invalidate(
        id_: int,
        group_id: str,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Id": group_id,
            },
        }

        return "ChangeGroup.Invalidate", payload_params

    @staticmethod
    def Poll(
        id_: int,
        group_id: str,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Id": group_id,
            },
        }

        return "ChangeGroup.Poll", payload_params

    @staticmethod
    def Remove(
        id_: int,
        group_id: str,
        controls: str | list[str],
    ) -> tuple[str, dict]:
        if isinstance(controls, str):
            controls = [controls]

        payload_params = {
            "id": id_,
            "params": {
                "Id": group_id,
                "Controls": controls,
            },
        }

        return "ChangeGroup.Remove", payload_params
