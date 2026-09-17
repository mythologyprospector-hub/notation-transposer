import json
from fractions import Fraction

import pytest

from notation_transposer.model import Duration, NTXDocument, Pitch
from notation_transposer.model.events import Note
from notation_transposer.model.serialization import dumps, loads, to_dict
from notation_transposer.model.structure import Measure, Part, Score, Staff, Voice
from notation_transposer.transform import transpose_document


def sample() -> NTXDocument:
    note = Note(Pitch("C", 4), Duration(Fraction(1, 4)), id="n1")
    voice = Voice(1, (note,))
    measure = Measure(1, (voice,))
    staff = Staff(1, "treble", (measure,))
    part = Part("P1", "Piano", (staff,))
    return NTXDocument(document_id="test-1", score=Score((part,)))


def test_pitch_preserves_spelling_information():
    assert Pitch("C", 4).midi_number == 60
    assert Pitch("C", 4, 1).midi_number == 61
    assert Pitch("D", 4, -1).midi_number == 61


def test_transpose_changes_pitch_not_rhythm_or_structure():
    doc = sample()
    result = transpose_document(doc, 2)
    event = result.score.parts[0].staves[0].measures[0].voices[0].events[0]
    assert event.pitch == Pitch("D", 4)
    assert event.duration == Duration(Fraction(1, 4))
    assert result.score.parts[0].id == "P1"


def test_transpose_preserves_negative_and_octave_crossing():
    assert Pitch("C", 4).transpose_chromatic(-1) == Pitch("B", 3)
    assert Pitch("B", 4).transpose_chromatic(1) == Pitch("C", 5)


def test_serialization_is_json_native_and_deterministic():
    first = dumps(sample())
    second = dumps(sample())
    assert first == second
    data = to_dict(sample())
    json.dumps(data)
    assert data["ntx_version"] == "0.1"
    assert first.endswith("\n")


def test_serialization_round_trip_reconstructs_document():
    doc = sample()
    assert loads(dumps(doc)) == doc


def test_deserialization_rejects_unsupported_major_version():
    data = to_dict(sample())
    data["ntx_version"] = "1.0"
    with pytest.raises(ValueError, match="unsupported NTX major version"):
        loads(json.dumps(data))


def test_invalid_document_id_rejected():
    try:
        NTXDocument(document_id="", score=Score())
    except ValueError as exc:
        assert "document id" in str(exc)
    else:
        raise AssertionError("empty document id was accepted")


def test_duplicate_part_ids_are_diagnostic():
    part = Part("P1", "Piano")
    doc = NTXDocument(document_id="test-duplicate", score=Score((part, part)))
    diagnostics = doc.validate()
    assert any(d.code == "DUPLICATE_PART_ID" and d.severity == "error" for d in diagnostics)
