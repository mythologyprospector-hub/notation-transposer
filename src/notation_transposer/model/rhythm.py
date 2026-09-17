from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True, slots=True)
class Duration:
    """Exact musical duration expressed as a fraction of a whole note."""

    value: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.value, Fraction):
            raise TypeError("Duration.value must be fractions.Fraction")
        if self.value <= 0:
            raise ValueError("duration must be positive")

    @classmethod
    def beats(cls, numerator: int, denominator: int = 4) -> "Duration":
        if numerator <= 0 or denominator <= 0:
            raise ValueError("duration components must be positive")
        return cls(Fraction(numerator, denominator))

    @classmethod
    def from_json(cls, value: str) -> "Duration":
        if "/" in value:
            numerator, denominator = value.split("/", 1)
            return cls(Fraction(int(numerator), int(denominator)))
        return cls(Fraction(value))

    def to_json(self) -> str:
        return f"{self.value.numerator}/{self.value.denominator}"


@dataclass(frozen=True, slots=True)
class TimeSignature:
    beats: int
    beat_type: int

    def __post_init__(self) -> None:
        if self.beats <= 0 or self.beat_type <= 0:
            raise ValueError("time signature values must be positive")
