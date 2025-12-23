from dataclasses import dataclass

@dataclass(frozen=True)
class StitchNode:
    name: str

@dataclass(frozen=True)
class RepeatNode:
    elements: list[StitchNode]
    num_times: int = None

@dataclass(frozen=True)
class RowNode:
    number: int
    instructions: list[StitchNode|RepeatNode]

@dataclass(frozen=True)
class PartNode:
    caston: int
    rows: list[RowNode]
    assumed_caston: bool = False