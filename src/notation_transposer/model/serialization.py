from __future__ import annotations

import json
from dataclasses import asdict
from fractions import Fraction

from .document import NTXDocument


def to_dict(document: NTXDocument) -> dict[str, object]:
    """Serialize an NTX document using only JSON-native values."""
    data = asdict(document)
    _convert(data)
    return data


def dumps(document: NTXDocument, *, indent: int = 2) -> str:
    return json.dumps(to_dict(document), indent=indent, ensure_ascii=False, sort_keys=True) + "\n"


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
