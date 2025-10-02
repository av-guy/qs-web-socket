class LoopPlayer:
    @staticmethod
    def Cancel(
        id_: int,
        name: str,
        outputs: list[int],
        log: bool = True,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Outputs": outputs,
                "Log": log,
            },
        }
        return "LoopPlayer.Cancel", payload_params

    @staticmethod
    def Start(
        id_: int,
        name: str,
        start_time: float,
        files: list[dict],
        loop: bool = False,
        log: bool = True,
        ref_id: str | None = None,
        seek: float | None = None,
    ) -> tuple[str, dict]:
        params: dict = {
            "Name": name,
            "StartTime": start_time,
            "Files": files,
            "Loop": loop,
            "Log": log,
        }

        if ref_id is not None:
            params["RefID"] = ref_id
        if seek is not None:
            params["Seek"] = seek

        payload_params = {"id": id_, "params": params}
        return "LoopPlayer.Start", payload_params

    @staticmethod
    def Stop(
        id_: int,
        name: str,
        outputs: list[int],
        log: bool = True,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Outputs": outputs,
                "Log": log,
            },
        }
        return "LoopPlayer.Stop", payload_params
