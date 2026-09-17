# Format Specification

**Status: LOCKED FOUNDATION**  
**Document version: 0.1**

## Format hierarchy

The project deliberately uses different formats for different jobs.

| Format | Role | Authority inside the project |
|---|---|---|
| NTX JSON | Canonical project document | **Primary** |
| MusicXML 4.0 | General notation interchange | External interchange |
| MEI | Scholarly/archive/high-fidelity notation | External interchange |
| ABC | Compact textual notation | External interchange |
| Plain-text tablature | Human-friendly tab input/output | External interchange |
| MIDI | Performance/control interchange | Secondary / validation |
| PDF/image | Recognition input | Evidence only |
| SVG/PNG/PDF rendering | Presentation output | Never canonical |

## Why NTX exists

No single external format should become the hidden center of the application.

MusicXML is the practical first interchange target and already covers score/part structures, concert/transposed contexts, and a broad set of notation semantics. The W3C Music Notation Community Group maintains the MusicXML specification and is actively working on subsequent revisions.

MEI is particularly appropriate for scholarly and archival representation because it is explicitly designed as a machine-readable model for complex musical documents, including structural and intellectual characteristics and multiple rendering possibilities.

The project's own model sits above these adapters so transformations do not become coupled to XML vocabulary or engraving layout.

## NTX JSON requirements

Every NTX document has, at minimum:

```json
{
  "ntx_version": "0.1",
  "document_id": "...",
  "metadata": {},
  "sources": [],
  "score": {},
  "diagnostics": [],
  "provenance": {}
}
```

The exact schema is to be implemented in `schema/` once the first domain model is built. This placeholder is intentional: the schema must emerge from tested domain objects rather than from a prematurely frozen pile of JSON fields.

### Required semantic concepts

The model must be capable of representing, where supplied:

- work identity and titles
- creators and attribution
- instruments and parts
- concert pitch and written pitch contexts
- key signatures
- time signatures
- clefs
- measures and rhythmic positions
- notes/rests/chords
- durations and tuplets
- voices
- ties and slurs
- beams
- articulations and ornaments
- dynamics and directions
- repeats and navigation
- lyrics
- staff-specific properties
- tablature tuning/string/fret information
- provenance and confidence
- unresolved ambiguity

## MusicXML policy

**MusicXML 4.0 is the first-class conventional-notation interchange target.**

The adapter should preserve the semantics needed for:

- scores and parts
- written/concert pitch contexts
- staff/voice structure
- rhythmic notation
- articulations and directions
- tablature technical information where available

The adapter must maintain a loss report for information that cannot be represented in NTX or cannot be represented faithfully in the selected MusicXML profile.

MusicXML's ecosystem is actively maintained, with work toward a 4.1 revision reported by the W3C Music Notation Community Group in August 2026.

## MEI policy

MEI is a supported high-fidelity interchange and archival path, not merely another parser.

The adapter should preserve scholarly/document characteristics where they map meaningfully into NTX and should expose information that NTX cannot yet represent instead of silently flattening it.

The project will target the currently documented MEI 5.x ecosystem rather than hard-coding an obsolete version into the architecture. Version-specific adapters may be introduced as compatibility requires.

## ABC policy

ABC is a convenience/text interchange format.

The adapter will support the subset that can map cleanly into NTX. ABC-specific constructs that have no semantic equivalent will be preserved as extension/provenance data where feasible or reported as loss.

ABC is not the internal representation.

## Tablature policy

Tablature gets its own adapter because a tab is not merely a pitch spelling.

For example, the same sounding pitch can occur on several strings/frets. Therefore:

```text
pitch → possible tab positions → constrained realization
```

is the correct conceptual model.

A tab input that contains explicit string/fret information is authoritative for that information. A tab generated from pitches is a derived realization and must be marked as such.

The first text-tab adapter should favor a conservative, well-defined grammar over trying to parse every internet tablature dialect.

## MIDI policy

MIDI can provide pitch, timing, velocity, channel, controller, and performance information, but it does not necessarily contain the notation semantics needed to reconstruct the original score.

Therefore MIDI import must produce an explicitly reconstructed document and must not claim to have recovered the original notation.

MIDI export is useful for checking that a transformed document produces the intended sounding material.

## Image/PDF policy

Images and PDFs are not notation formats for the core. They are evidence sources for recognition.

A future recognizer should produce:

```text
source image/PDF
      ↓
recognized candidates
      ↓
NTX + confidence + provenance + unresolved ambiguity
```

A successful recognition run is not equivalent to a verified transcription.

## Rendering policy

Rendering outputs include SVG, PDF, PNG, terminal/TUI views, and potentially browser views.

These are generated views of NTX. They are never authoritative musical data.

SMuFL is treated as a rendering-layer standard for music glyphs.

## Round-trip guarantee levels

Adapters use explicit guarantee levels:

- **Exact** — semantic content can be round-tripped without known loss.
- **Equivalent** — the representation may differ but musical meaning is preserved.
- **Best effort** — some semantics may be lost or normalized.
- **Lossy** — the operation intentionally discards information.
- **Reconstructed** — information was inferred from an incomplete/performance source.

No adapter may advertise a stronger guarantee than its tests demonstrate.
