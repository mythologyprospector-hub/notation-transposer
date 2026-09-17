from __future__ import annotations

from dataclasses import replace

from ..model.document import NTXDocument
from ..model.events import Chord, Note
from ..model.structure import Measure, Part, Score, Staff, Voice


def transpose_document(document: NTXDocument, semitones: int) -> NTXDocument:
    """Return a deterministically chromatically transposed document.

    Notated spelling is recalculated from the resulting pitch. Rhythm and structure
    are preserved. The operation does not invent tablature positions.
    """
    if not isinstance(semitones, int):
        raise TypeError("semitones must be an integer")

    parts = tuple(
        replace(part, staves=tuple(_transpose_staff(staff, semitones) for staff in part.staves))
        for part in document.score.parts
    )
    return replace(
        document,
        score=Score(parts=parts),
        provenance={
            **document.provenance,
            "last_transformation": {
                "operation": "chromatic_transpose",
                "semitones": semitones,
                "deterministic": True,
            },
        },
    )


def _transpose_staff(staff: Staff, semitones: int) -> Staff:
    return replace(staff, measures=tuple(_transpose_measure(m, semitones) for m in staff.measures))


def _transpose_measure(measure: Measure, semitones: int) -> Measure:
    return replace(measure, voices=tuple(_transpose_voice(v, semitones) for v in measure.voices))


def _transpose_voice(voice: Voice, semitones: int) -> Voice:
    events = []
    for event in voice.events:
        if isinstance(event, Note):
            events.append(replace(event, pitch=event.pitch.transpose_chromatic(semitones)))
        elif isinstance(event, Chord):
            events.append(replace(event, notes=tuple(replace(n, pitch=n.pitch.transpose_chromatic(semitones)) for n in event.notes)))
        else:
            events.append(event)
    return replace(voice, events=tuple(events))
