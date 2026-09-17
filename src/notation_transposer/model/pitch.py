from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Step = Literal["C", "D", "E", "F", "G", "A", "B"]

_BASE_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_STEP_ORDER = ("C", "D", "E", "F", "G", "A", "B")


@dataclass(frozen=True, slots=True)
class Pitch:
    """A notated pitch: sounding pitch plus explicit diatonic spelling."""

    step: Step
    octave: int
    alter: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.octave, int):
            raise TypeError("octave must be an integer")
        if not isinstance(self.alter, int):
            raise TypeError("alter must be an integer")
        if self.alter < -2 or self.alter > 2:
            raise ValueError("alter must be between -2 and 2 semitones")

    @property
    def midi_number(self) -> int:
        return 12 * (self.octave + 1) + _BASE_PC[self.step] + self.alter

    @property
    def chromatic_class(self) -> int:
        return self.midi_number % 12

    def transpose_chromatic(self, semitones: int, *, preserve_spelling: bool = False) -> "Pitch":
        if not isinstance(semitones, int):
            raise TypeError("semitones must be an integer")
        if preserve_spelling:
            target_midi = self.midi_number + semitones
            octave, pc = divmod(target_midi, 12)
            octave -= 1
            natural = _BASE_PC[self.step]
            raw_alter = pc - natural
            while raw_alter > 6:
                raw_alter -= 12
                octave += 1
            while raw_alter < -6:
                raw_alter += 12
                octave -= 1
            if raw_alter < -2 or raw_alter > 2:
                raise ValueError("requested spelling cannot be represented with at most double accidentals")
            return Pitch(self.step, octave, raw_alter)
        target = self.midi_number + semitones
        octave, pc = divmod(target, 12)
        octave -= 1
        step = min(_STEP_ORDER, key=lambda s: abs((_BASE_PC[s] - pc + 6) % 12 - 6))
        delta = pc - _BASE_PC[step]
        if delta > 6:
            delta -= 12
        if delta < -6:
            delta += 12
        if delta < -2 or delta > 2:
            # Choose the enharmonic spelling nearest the target pitch with a legal accidental.
            candidates = [(s, pc - _BASE_PC[s]) for s in _STEP_ORDER]
            legal = [(s, d) for s, d in candidates if -2 <= d <= 2]
            if not legal:
                raise ValueError("cannot represent transposed pitch with supported accidentals")
            step, delta = min(legal, key=lambda item: abs(item[1]))
        return Pitch(step, octave, delta)
