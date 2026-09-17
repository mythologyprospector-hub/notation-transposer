from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .pitch import Pitch
from .rhythm import Duration

ProvenanceKind = Literal["source", "derived", "inferred", "user_asserted", "unknown"]


@dataclass(frozen=True, slots=True)
class Provenance:
    kind: ProvenanceKind
    source_id: str | None = None
    detail: str | None = None


@dataclass(frozen=True, slots=True)
class TabPosition:
    string: int
    fret: int
    course: int | None = None

    def __post_init__(self) -> None:
        if self.string < 1:
            raise ValueError("string must be >= 1")
        if self.fret < 0:
            raise ValueError("fret must be >= 0")
        if self.course is not None and self.course < 1:
            raise ValueError("course must be >= 1")


@dataclass(frozen=True, slots=True)
class TabRealization:
    tuning: tuple[Pitch, ...]
    positions: tuple[TabPosition, ...]
    capo: int = 0
    provenance: Provenance = field(default_factory=lambda: Provenance("derived"))

    def __post_init__(self) -> None:
        if not self.tuning:
            raise ValueError("tablature tuning cannot be empty")
        if self.capo < 0:
            raise ValueError("capo must be >= 0")


@dataclass(frozen=True, slots=True)
class Note:
    pitch: Pitch
    duration: Duration
    id: str
    voice: int = 1
    tab: tuple[TabRealization, ...] = ()
    provenance: Provenance = field(default_factory=lambda: Provenance("source"))


@dataclass(frozen=True, slots=True)
class Rest:
    duration: Duration
    id: str
    voice: int = 1
    provenance: Provenance = field(default_factory=lambda: Provenance("source"))


@dataclass(frozen=True, slots=True)
class Chord:
    notes: tuple[Note, ...]
    id: str
    provenance: Provenance = field(default_factory=lambda: Provenance("source"))

    def __post_init__(self) -> None:
        if not self.notes:
            raise ValueError("chord must contain at least one note")
