from __future__ import annotations

from dataclasses import dataclass, field

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


@dataclass(frozen=True, slots=True)
class NTXDocument:
    document_id: str
    score: Score
    metadata: dict[str, object] = field(default_factory=dict)
    sources: tuple[Source, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()
    provenance: dict[str, object] = field(default_factory=dict)
    ntx_version: str = "0.1"

    def __post_init__(self) -> None:
        if not self.document_id.strip():
            raise ValueError("document_id cannot be empty")
        if self.ntx_version.split(".")[0] != "0":
            raise ValueError("unsupported NTX major version")

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = list(self.diagnostics)
        seen_parts: set[str] = set()
        for part in self.score.parts:
            if part.id in seen_parts:
                diagnostics.append(Diagnostic("DUPLICATE_PART_ID", f"duplicate part id: {part.id}", "error"))
            seen_parts.add(part.id)
            seen_measures: set[int] = set()
            for staff in part.staves:
                for measure in staff.measures:
                    if measure.number in seen_measures:
                        diagnostics.append(Diagnostic("DUPLICATE_MEASURE", f"duplicate measure {measure.number} on staff {staff.number}", "error"))
                    seen_measures.add(measure.number)
        return tuple(diagnostics)
