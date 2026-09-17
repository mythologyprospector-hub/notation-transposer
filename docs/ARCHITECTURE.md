# Architecture

**Status: LOCKED FOUNDATION**  
**Document version: 0.1**

This document establishes the initial architecture of `notation-transposer`. Changes to these boundaries require an explicit architectural decision rather than accidental drift.

## 1. Core principle

The system is a **musical document transformation engine**, not a file-format converter with musical operations bolted on.

The canonical object is an NTX Document. Every supported external representation is converted into that model before transformation, and transformations operate on the model rather than directly on XML, text, or rendering coordinates.

## 2. Layers

### Layer A — Domain model

`ntx.model`

Owns musical meaning:

- document and metadata
- work/score/part/staff/voice hierarchy
- measures and rhythmic positions
- pitched and unpitched events
- duration and time signatures
- key signatures and transposition context
- clefs
- ties, slurs, tuplets, beams, repeats
- articulations, ornaments, dynamics, directions
- lyrics and annotations
- tablature positions: string, fret, course, tuning, capo, and technique
- provenance and uncertainty

The model must not depend on a particular parser, renderer, UI toolkit, or external file format.

### Layer B — Semantic operations

`ntx.transform`

Operations include:

- pitch transposition
- key/context transposition
- clef changes
- staff ↔ tablature mapping
- instrument-aware rewriting
- normalization
- structural comparison
- semantic validation

Operations consume and produce NTX Documents or well-defined document fragments.

### Layer C — Format adapters

`ntx.formats`

Each adapter has a narrow contract:

```text
external representation
        ↓
    parse/import
        ↓
     NTX Document
        ↓
    export/render
        ↓
external representation
```

Initial adapters:

- `musicxml`
- `mei`
- `abc`
- `tablature`
- `midi`

Adapters must declare preservation limitations. They may not silently discard information without recording that loss where practical.

### Layer D — Recognition / transcription

`ntx.recognition`

This is intentionally separate from deterministic notation transformation.

Future image/PDF/scanned-score recognition may produce an NTX Document containing confidence, provenance, and unresolved decisions. Recognition output is never treated as equivalent to authoritative structured notation merely because parsing succeeded.

### Layer E — Presentation

`ntx.render` and the TUI/API layers sit above the domain and transformation layers.

Presentation may show:

- staff notation
- tablature
- diagnostics
- before/after comparisons
- provenance and confidence
- transformation plans

Presentation must not become the source of truth.

## 3. Canonical NTX Document

The canonical serialized interchange for the project's own work products is **JSON**, with a versioned schema.

Recommended filename:

```text
<name>.ntx.json
```

The JSON representation is a serialization of the domain model, not a UI state dump.

Schema evolution uses an explicit document-model version. Readers should reject unsupported major versions rather than guessing how to interpret them.

## 4. Identity and provenance

Every imported fact should be traceable to its source when the adapter can provide that information.

The model distinguishes:

- `source` — supplied by the input
- `derived` — deterministically calculated from supplied data
- `inferred` — selected through a heuristic or recognition process
- `user_asserted` — explicitly chosen by a user
- `unknown` — unavailable

This distinction is critical for transcription. A system that cannot tell the difference between “the score said this” and “we guessed this” is not trustworthy enough for serious notation work.

## 5. Ambiguity policy

The engine does not silently resolve underdetermined musical questions.

Examples:

- A pitch can map to multiple tablature positions.
- A scanned symbol may have multiple plausible interpretations.
- An instrument tuning may be absent.
- Enharmonic spelling may depend on musical context.
- A source format may not carry enough information to reconstruct the original engraving.

Such cases produce an explicit diagnostic and, where possible, a set of candidate resolutions.

## 6. Transformation contract

A transformation must declare:

- operation name
- input document identity/version
- parameters
- policy choices
- deterministic result
- diagnostics
- information-loss report

A transformation should be replayable from its recorded parameters.

## 7. Tablature model

Tablature is treated as a first-class representation, not as text attached to a note.

A tab event may contain:

- instrument/tuning identity
- string or course
- fret
- capo context
- fingering
- bend/slide/hammer/pull-off and other techniques
- simultaneous string events
- rhythmic relationship to the underlying musical event

The engine may represent multiple valid tab realizations for the same pitched material. Selection of a realization is a policy problem, not a property of pitch alone.

## 8. MIDI boundary

MIDI represents performance/control information rather than complete notation semantics. It is therefore an adapter and validation aid, not the canonical source for notation.

A MIDI import may reconstruct approximate rhythmic/pitch material, but it must not manufacture notation semantics such as original beaming, engraving intent, articulation intent, or exact enharmonic spelling unless supplied elsewhere.

## 9. Rendering boundary

The core does not store font glyph names, pixel coordinates, line breaks, page geometry, or renderer-specific layout instructions as musical truth.

A renderer consumes NTX and decides how to display it. SMuFL-compatible notation fonts are a rendering concern.

## 10. Determinism

Core transformations must be deterministic by default. If a heuristic search or recognition system introduces nondeterminism, that fact must be explicit and its policy/configuration captured in the result metadata.

## 11. Testing strategy

Tests are divided into:

1. **Model invariants** — invalid musical structures are rejected.
2. **Transformation tests** — known musical transformations produce expected semantics.
3. **Round-trip tests** — supported formats survive import/export within documented limits.
4. **Golden documents** — representative scores and tabs exercise difficult structures.
5. **Loss tests** — adapters explicitly identify information they cannot preserve.
6. **Property tests** — transformations obey algebraic expectations where applicable.
7. **Recognition tests** — confidence and ambiguity behavior are tested separately from deterministic parsing.

## 12. Repository structure

The intended source tree is:

```text
src/notation_transposer/
    model/
    transform/
    formats/
        musicxml/
        mei/
        abc/
        tablature/
        midi/
    recognition/
    render/
    diagnostics/
    cli/

tests/
    unit/
    integration/
    golden/
    fixtures/

docs/
    ARCHITECTURE.md
    FORMAT-SPEC.md
    DECISIONS/
```

The exact Python module names may evolve, but the dependency direction does not:

```text
presentation → transforms → model ← adapters
recognition → model
render → model
```

The domain model remains the center and does not import upward into UI or adapters.

## 13. Dependencies

Prefer small, mature, permissively licensed dependencies. External libraries are adapters/helpers, not architectural authorities.

A dependency that becomes the de facto domain model must be treated as an architectural change and reviewed explicitly.

## 14. Architectural non-goals

At this stage we are **not** committing to:

- a full notation editor
- automatic perfect score recognition
- one “best” tablature fingering algorithm
- a proprietary project file format
- a browser-only implementation
- MIDI-first processing
- renderer-specific musical semantics

Those can be built above this foundation without changing what the foundation means.
