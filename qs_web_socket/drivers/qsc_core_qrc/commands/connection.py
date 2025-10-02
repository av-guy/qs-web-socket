class Connection:
    @staticmethod
    def Logon(user: str, password: str, id_: int | None = None) -> tuple[str, dict]:
        payload_params: dict = {
            "params": {"User": user, "Password": password}
        }

        if id_ is not None:
            payload_params["id"] = id_

        return "Logon", payload_params

    @staticmethod
    def NoOp() -> tuple[str, dict]:
        payload_params = {}
        return "NoOp", payload_params
