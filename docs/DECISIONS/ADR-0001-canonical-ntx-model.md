# ADR-0001: Canonical NTX Model

**Status:** Accepted  
**Date:** 2026-09-17

## Decision

`notation-transposer` will use a project-owned, versioned **NTX Document Model** as its canonical internal representation.

External notation formats will be implemented as adapters around that model.

## Context

The project must operate across staff notation, full scores, parts, and tablature. It may eventually ingest notation from structured files, text, MIDI, scans, and images.

Choosing one external format as the internal model would make the transformation engine inherit that format's assumptions and limitations.

## Consequences

### Positive

- Musical operations remain independent of file formats.
- Tablature can be represented as a first-class realization rather than forced into a staff-only model.
- Provenance and uncertainty can be represented consistently.
- New formats can be added without rewriting the transformation engine.
- Rendering remains separate from musical semantics.

### Costs

- We must design and maintain our own domain model.
- Every external format requires an adapter.
- Some information will require explicit extension mechanisms.
- Round-trip behavior must be tested per adapter.

## Rejected alternatives

### MusicXML as the internal model

Rejected because it would make an interchange format the architectural center and would make tablature, provenance, uncertainty, and future recognition harder to model cleanly.

### MIDI as the internal model

Rejected because MIDI is performance-oriented and does not preserve enough notation semantics to serve as the source of truth for scores.

### Renderer-first representation

Rejected because engraving/layout coordinates are presentation, not musical meaning.

## Review trigger

Revisit this decision only if the NTX model proves unable to represent a required musical domain without becoming a thin copy of an existing standard. That failure must be demonstrated with concrete cases before changing the architecture.
