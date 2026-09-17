from __future__ import annotations

import json
from dataclasses import asdict
from fractions import Fraction
from typing import Any

from .document import NTXDocument
from .events import Chord, Note, Provenance, Rest, TabPosition, TabRealization
from .pitch import Pitch
from .rhythm import Duration, TimeSignature
from .structure import Diagnostic, Measure, Part, Score, Source, Staff, Voice


def to_dict(document: NTXDocument) -> dict[str, object]:
    """Serialize an NTX document using only JSON-native values."""
    data = asdict(document)
    _convert(data)
    return data


def dumps(document: NTXDocument, *, indent: int = 2) -> str:
    """Serialize an NTX document to deterministic JSON text."""
    return json.dumps(to_dict(document), indent=indent, ensure_ascii=False, sort_keys=True) + "\n"


def loads(text: str) -> NTXDocument:
    """Deserialize an NTX document from JSON text.

    The NTX major version is checked by ``NTXDocument``; unsupported major
    versions therefore fail rather than being guessed into the current model.
    """
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("NTX JSON root must be an object")
    return from_dict(data)


def from_dict(data: dict[str, Any]) -> NTXDocument:
    """Deserialize a JSON-native NTX mapping into the domain model."""
    required = ("ntx_version", "document_id", "score")
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"missing required NTX fields: {', '.join(missing)}")

    score_data = _mapping(data["score"], "score")
    parts = tuple(_part(item) for item in _sequence(score_data.get("parts", ()), "score.parts"))

    sources = tuple(_source(item) for item in _sequence(data.get("sources", ()), "sources"))
    diagnostics = tuple(_diagnostic(item) for item in _sequence(data.get("diagnostics", ()), "diagnostics"))

    metadata = _mapping(data.get("metadata", {}), "metadata")
    provenance = _mapping(data.get("provenance", {}), "provenance")

    return NTXDocument(
        document_id=_string(data["document_id"], "document_id"),
        score=Score(parts=parts),
        metadata=metadata,
        sources=sources,
        diagnostics=diagnostics,
        provenance=provenance,
        ntx_version=_string(data["ntx_version"], "ntx_version"),
    )


def _part(value: Any) -> Part:
    data = _mapping(value, "part")
    return Part(
        id=_string(data["id"], "part.id"),
        name=_string(data["name"], "part.name"),
        staves=tuple(_staff(item) for item in _sequence(data.get("staves", ()), "part.staves")),
        instrument=_optional_string(data.get("instrument"), "part.instrument"),
        transposition_semitones=int(data.get("transposition_semitones", 0)),
    )


def _staff(value: Any) -> Staff:
    data = _mapping(value, "staff")
    return Staff(
        number=int(data["number"]),
        clef=_optional_string(data.get("clef"), "staff.clef"),
        measures=tuple(_measure(item) for item in _sequence(data.get("measures", ()), "staff.measures")),
    )


def _measure(value: Any) -> Measure:
    data = _mapping(value, "measure")
    time_data = data.get("time_signature")
    time_signature = None
    if time_data is not None:
        ts = _mapping(time_data, "measure.time_signature")
        time_signature = TimeSignature(beats=int(ts["beats"]), beat_type=int(ts["beat_type"]))
    return Measure(
        number=int(data["number"]),
        voices=tuple(_voice(item) for item in _sequence(data.get("voices", ()), "measure.voices")),
        time_signature=time_signature,
        pickup=bool(data.get("pickup", False)),
    )


def _voice(value: Any) -> Voice:
    data = _mapping(value, "voice")
    return Voice(
        number=int(data["number"]),
        events=tuple(_event(item) for item in _sequence(data.get("events", ()), "voice.events")),
    )


def _event(value: Any) -> Note | Rest | Chord:
    data = _mapping(value, "event")
    if "pitch" in data:
        return _note(data)
    if "notes" in data:
        return Chord(
            notes=tuple(_note(item) for item in _sequence(data["notes"], "chord.notes")),
            id=_string(data["id"], "chord.id"),
            provenance=_provenance(data.get("provenance", {})),
        )
    if "duration" in data:
        return Rest(
            duration=Duration.from_json(_string(data["duration"], "rest.duration")),
            id=_string(data["id"], "rest.id"),
            voice=int(data.get("voice", 1)),
            provenance=_provenance(data.get("provenance", {})),
        )
    raise ValueError("event must contain pitch, notes, or duration")


def _note(data: dict[str, Any]) -> Note:
    pitch_data = _mapping(data["pitch"], "note.pitch")
    pitch = Pitch(
        step=_string(pitch_data["step"], "note.pitch.step"),
        octave=int(pitch_data["octave"]),
        alter=int(pitch_data.get("alter", 0)),
    )
    tab = tuple(_tab_realization(item) for item in _sequence(data.get("tab", ()), "note.tab"))
    return Note(
        pitch=pitch,
        duration=Duration.from_json(_string(data["duration"], "note.duration")),
        id=_string(data["id"], "note.id"),
        voice=int(data.get("voice", 1)),
        tab=tab,
        provenance=_provenance(data.get("provenance", {})),
    )


def _tab_realization(value: Any) -> TabRealization:
    data = _mapping(value, "tab")
    tuning = tuple(_pitch(item) for item in _sequence(data["tuning"], "tab.tuning"))
    positions = tuple(_tab_position(item) for item in _sequence(data["positions"], "tab.positions"))
    return TabRealization(
        tuning=tuning,
        positions=positions,
        capo=int(data.get("capo", 0)),
        provenance=_provenance(data.get("provenance", {})),
    )


def _pitch(value: Any) -> Pitch:
    data = _mapping(value, "pitch")
    return Pitch(
        step=_string(data["step"], "pitch.step"),
        octave=int(data["octave"]),
        alter=int(data.get("alter", 0)),
    )


def _tab_position(value: Any) -> TabPosition:
    data = _mapping(value, "tab position")
    return TabPosition(
        string=int(data["string"]),
        fret=int(data["fret"]),
        course=None if data.get("course") is None else int(data["course"]),
    )


def _provenance(value: Any) -> Provenance:
    data = _mapping(value, "provenance")
    return Provenance(
        kind=_string(data.get("kind", "unknown"), "provenance.kind"),
        source_id=_optional_string(data.get("source_id"), "provenance.source_id"),
        detail=_optional_string(data.get("detail"), "provenance.detail"),
    )


def _source(value: Any) -> Source:
    data = _mapping(value, "source")
    return Source(
        id=_string(data["id"], "source.id"),
        kind=_string(data["kind"], "source.kind"),
        location=_optional_string(data.get("location"), "source.location"),
        checksum=_optional_string(data.get("checksum"), "source.checksum"),
    )


def _diagnostic(value: Any) -> Diagnostic:
    data = _mapping(value, "diagnostic")
    return Diagnostic(
        code=_string(data["code"], "diagnostic.code"),
        message=_string(data["message"], "diagnostic.message"),
        severity=_string(data.get("severity", "warning"), "diagnostic.severity"),
        path=_optional_string(data.get("path"), "diagnostic.path"),
    )


def _mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _sequence(value: Any, name: str) -> list[Any] | tuple[Any, ...]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be an array")
    return value


def _string(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def _optional_string(value: Any, name: str) -> str | None:
    if value is None:
        return None
    return _string(value, name)


def _convert(value: object) -> object:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        for key in list(value):
            value[key] = _convert(value[key])
        return value
    if isinstance(value, list):
        for i, item in enumerate(value):
            value[i] = _convert(item)
        return value
    return value
