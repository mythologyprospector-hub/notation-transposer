from __future__ import annotations

from dataclasses import dataclass, field

from .events import Chord, Note, Rest
from .structure import Score, Source, Diagnostic


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
        try:
            major = int(self.ntx_version.split(".", 1)[0])
        except (ValueError, IndexError) as exc:
            raise ValueError("invalid NTX version") from exc
        if major != 0:
            raise ValueError("unsupported NTX major version")

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = list(self.diagnostics)
        seen_parts: set[str] = set()
        for part in self.score.parts:
            if part.id in seen_parts:
                diagnostics.append(Diagnostic("DUPLICATE_PART_ID", f"duplicate part id: {part.id}", "error"))
            seen_parts.add(part.id)
            for staff in part.staves:
                seen_measures: set[int] = set()
                for measure in staff.measures:
                    if measure.number in seen_measures:
                        diagnostics.append(Diagnostic("DUPLICATE_MEASURE", f"duplicate measure {measure.number} on staff {staff.number}", "error"))
                    seen_measures.add(measure.number)
        return tuple(diagnostics)
