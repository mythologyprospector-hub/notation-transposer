from __future__ import annotations

from dataclasses import dataclass

from .events import Chord, Note, Rest
from .rhythm import TimeSignature

Event = Note | Rest | Chord


@dataclass(frozen=True, slots=True)
class Voice:
    number: int
    events: tuple[Event, ...] = ()

    def __post_init__(self) -> None:
        if self.number < 1:
            raise ValueError("voice number must be >= 1")


@dataclass(frozen=True, slots=True)
class Measure:
    number: int
    voices: tuple[Voice, ...] = ()
    time_signature: TimeSignature | None = None
    pickup: bool = False

    def __post_init__(self) -> None:
        if self.number < 1:
            raise ValueError("measure number must be >= 1")


@dataclass(frozen=True, slots=True)
class Staff:
    number: int
    clef: str | None = None
    measures: tuple[Measure, ...] = ()

    def __post_init__(self) -> None:
        if self.number < 1:
            raise ValueError("staff number must be >= 1")


@dataclass(frozen=True, slots=True)
class Part:
    id: str
    name: str
    staves: tuple[Staff, ...] = ()
    instrument: str | None = None
    transposition_semitones: int = 0

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("part id cannot be empty")


@dataclass(frozen=True, slots=True)
class Score:
    parts: tuple[Part, ...] = ()


@dataclass(frozen=True, slots=True)
class Source:
    id: str
    kind: str
    location: str | None = None
    checksum: str | None = None


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    message: str
    severity: str = "warning"
    path: str | None = None
