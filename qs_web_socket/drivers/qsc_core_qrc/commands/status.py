class Status:
    @staticmethod
    def StatusGet(id_: int) -> tuple[str, dict]:
        payload_params = {"id": id_, "params": 0}
        return "StatusGet", payload_params
