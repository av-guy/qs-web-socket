class Snapshot:
    @staticmethod
    def Load(
        id_: int,
        name: str,
        bank: int,
        ramp: float | None = None,
    ) -> tuple[str, dict]:
        params: dict = {
            "Name": name,
            "Bank": bank,
        }
        if ramp is not None:
            params["Ramp"] = ramp

        payload_params = {"id": id_, "params": params}
        return "Snapshot.Load", payload_params

    @staticmethod
    def Save(
        id_: int,
        name: str,
        bank: int,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Bank": bank,
            },
        }
        return "Snapshot.Save", payload_params
