from typing import Iterable, Literal


class ChannelSpec:
    def __init__(
        self,
        include: Iterable[int] | str | int | range,
        exclude: Iterable[int] | None = None
    ):
        self.include = include
        self.exclude = exclude or []


    def __str__(self) -> str:
        if isinstance(self.include, ChannelSpec):
            include_str = str(self.include)
        elif isinstance(self.include, str):
            include_str = self.include
        else:
            include_str = _format_channel_spec(self.include)

        if self.exclude:
            if isinstance(self.exclude, ChannelSpec):
                exclude_str = str(self.exclude)
            else:
                exclude_str = _format_channel_spec(self.exclude)
            return f"{include_str} !{exclude_str}"

        return include_str


def _format_channel_spec(spec: int | Iterable[int]) -> str:
    if isinstance(spec, int):
        return str(spec)

    values = sorted(set(list(spec)))
    if not values:
        return ""

    parts: list[str] = []
    start = prev = values[0]

    for v in values[1:]:
        if v == prev + 1:
            prev = v
            continue

        if start == prev:
            parts.append(str(start))
        else:
            parts.append(f"{start}-{prev}")

        start = prev = v

    if start == prev:
        parts.append(str(start))
    else:
        parts.append(f"{start}-{prev}")

    return " ".join(parts)


def _normalize_channels(ch: ChannelSpec | int | list[int] | range | Literal["*"] | str) -> str:
    if isinstance(ch, ChannelSpec):
        return str(ch)
    if isinstance(ch, (int, list, range)):
        return _format_channel_spec(ch)
    return str(ch)


class Mixer:
    @staticmethod
    def SetCrossPointDelay(
        id_: int,
        name: str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        outputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: float,
        ramp: float,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Inputs": _normalize_channels(inputs),
                "Outputs": _normalize_channels(outputs),
                "Value": value,
                "Ramp": ramp,
            },
        }
        return "Mixer.SetCrossPointDelay", payload_params

    @staticmethod
    def SetCrossPointGain(
        id_: int,
        name: str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        outputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: float,
        ramp: float,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Inputs": _normalize_channels(inputs),
                "Outputs": _normalize_channels(outputs),
                "Value": value,
                "Ramp": ramp,
            },
        }
        return "Mixer.SetCrossPointGain", payload_params

    @staticmethod
    def SetCrossPointMute(
        id_: int,
        name: str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        outputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: bool,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Inputs": _normalize_channels(inputs),
                "Outputs": _normalize_channels(outputs),
                "Value": value,
            },
        }
        return "Mixer.SetCrossPointMute", payload_params

    @staticmethod
    def SetCrossPointSolo(
        id_: int,
        name: str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        outputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: bool,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Inputs": _normalize_channels(inputs),
                "Outputs": _normalize_channels(outputs),
                "Value": value,
            },
        }
        return "Mixer.SetCrossPointSolo", payload_params

    @staticmethod
    def SetCueGain(
        id_: int,
        name: str,
        cues: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: float,
        ramp: float,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Cues": _normalize_channels(cues),
                "Value": value,
                "Ramp": ramp,
            },
        }
        return "Mixer.SetCueGain", payload_params

    @staticmethod
    def SetCueMute(
        id_: int,
        name: str,
        cues: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: bool,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Cues": _normalize_channels(cues),
                "Value": value,
            },
        }
        return "Mixer.SetCueMute", payload_params

    @staticmethod
    def SetInputCueAfl(
        id_: int,
        name: str,
        cues: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: bool,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Cues": _normalize_channels(cues),
                "Inputs": _normalize_channels(inputs),
                "Value": value,
            },
        }
        return "Mixer.SetInputCueAfl", payload_params

    @staticmethod
    def SetInputCueEnable(
        id_: int,
        name: str,
        cues: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: bool,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Cues": _normalize_channels(cues),
                "Inputs": _normalize_channels(inputs),
                "Value": value,
            },
        }
        return "Mixer.SetInputCueEnable", payload_params

    @staticmethod
    def SetInputGain(
        id_: int,
        name: str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: float,
        ramp: float,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Inputs": _normalize_channels(inputs),
                "Value": value,
                "Ramp": ramp,
            },
        }
        return "Mixer.SetInputGain", payload_params

    @staticmethod
    def SetInputMute(
        id_: int,
        name: str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: bool,
        ramp: float = 0.0,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Inputs": _normalize_channels(inputs),
                "Value": value,
                "Ramp": ramp,
            },
        }
        return "Mixer.SetInputMute", payload_params

    @staticmethod
    def SetInputSolo(
        id_: int,
        name: str,
        inputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: bool,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Inputs": _normalize_channels(inputs),
                "Value": value,
            },
        }
        return "Mixer.SetInputSolo", payload_params

    @staticmethod
    def SetOutputGain(
        id_: int,
        name: str,
        outputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: float,
        ramp: float,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Outputs": _normalize_channels(outputs),
                "Value": value,
                "Ramp": ramp,
            },
        }
        return "Mixer.SetOutputGain", payload_params

    @staticmethod
    def SetOutputMute(
        id_: int,
        name: str,
        outputs: ChannelSpec | int | list[int] | range | Literal["*"] | str,
        value: bool,
    ) -> tuple[str, dict]:
        payload_params = {
            "id": id_,
            "params": {
                "Name": name,
                "Outputs": _normalize_channels(outputs),
                "Value": value,
            },
        }
        return "Mixer.SetOutputMute", payload_params


ALL = ChannelSpec("*")
NONE = ChannelSpec([])
