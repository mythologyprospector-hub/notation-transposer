import json
from fractions import Fraction

from notation_transposer.model import Duration, NTXDocument, Pitch
from notation_transposer.model.document import Score
from notation_transposer.model.events import Note
from notation_transposer.model.structure import Measure, Part, Staff, Voice
from notation_transposer.model.serialization import dumps, to_dict
from notation_transposer.transform import transpose_document


def sample() -> NTXDocument:
    note = Note(Pitch("C", 4), Duration(Fraction(1, 4)), id="n1")
    return NTXDocument(
        document_id="test-1",
        score=Score((Part("P1", "Piano", (Staff(1, "treble", (Measure(1, (Voice(1, (note,)),)),)),)),)),)),
    )


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


def test_serialization_is_json_native():
    data = to_dict(sample())
    json.dumps(data)
    assert data["ntx_version"] == "0.1"
    assert dumps(sample()).endswith("\n")


def test_invalid_document_id_rejected():
    try:
        NTXDocument(document_id="", score=Score())
    except ValueError as exc:
        assert "document_id" in str(exc)
    else:
        raise AssertionError("empty document id was accepted")
