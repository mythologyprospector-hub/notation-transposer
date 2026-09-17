# notation-transposer

A notation-first toolkit for **transposing and transcribing musical staff notation, scores, and tablature**.

The project is deliberately built around a canonical musical representation rather than around any single file format or notation editor. External formats are adapters; musical meaning lives in the core model.

## What this is for

- Transpose music between keys, clefs, and instrument contexts.
- Translate between staff notation and tablature where the source contains enough information to do so.
- Preserve voices, rhythm, articulations, dynamics, tuplets, repeats, lyrics, and instrument-specific information whenever the source format permits it.
- Make uncertainty explicit instead of silently inventing musical information.
- Produce interoperable notation files rather than trapping the work in a proprietary representation.

## Canonical format policy

The project uses a versioned internal **NTX Document Model** as its canonical working representation.

Supported external formats are treated as adapters:

- **MusicXML 4.0** — primary interchange format for conventional notation and score/part exchange.
- **MEI** — archival/scholarly interchange and high-fidelity notation representation.
- **ABC notation** — lightweight textual import/export where its model is sufficient.
- **Plain-text tablature** — import/export through an explicit tab adapter; never treated as the canonical model.
- **MIDI** — performance-oriented input/output and validation aid, not a notation source of truth.
- **Images/PDF** — future transcription inputs; recognition is an ingestion layer and must emit uncertainty/provenance rather than pretending OCR is authoritative.

Rendering is deliberately separate from musical transformation. SMuFL-compatible glyph systems may be used by renderers, but glyph choice is not part of the canonical musical model.

## Architecture

```text
                 +----------------------+
                 |   User / TUI / API   |
                 +----------+-----------+
                            |
                    Application layer
                            |
                 +----------v-----------+
                 |   Transformation     |
                 | transpose / map /    |
                 | validate / compare   |
                 +----------+-----------+
                            |
                 +----------v-----------+
                 |    NTX Document      |
                 |   Canonical Model    |
                 +----+----+----+-------+
                      |    |    |
          +-----------+    |    +-------------+
          |                |                  |
    Import adapters   Validation        Export adapters
          |                |                  |
   MusicXML / MEI /    invariants       MusicXML / MEI /
   ABC / Tab / MIDI                    ABC / Tab / MIDI
          |
    Future recognition
    PDF / image / scan
```

The detailed architectural contract is in `docs/ARCHITECTURE.md`. The format contract is in `docs/FORMAT-SPEC.md`.

## Design rules

1. **Musical semantics before presentation.** Staff position, glyphs, spacing, and layout are representations of music, not the music itself.
2. **No silent guessing.** Ambiguity becomes an explicit diagnostic or unresolved choice.
3. **Round-trip awareness.** Adapters report what information they can preserve and what they cannot.
4. **Source provenance matters.** Imported and inferred facts remain distinguishable.
5. **Deterministic transformations.** Given the same document, operation, and policy, the result should be reproducible.
6. **Format neutrality.** No external notation format is allowed to become the hidden internal model.
7. **Tests protect musical meaning.** Structural and semantic tests are more important than screenshots.

## Status

The repository is in the **foundation phase**. The architecture and document-format policy are intentionally being established before feature growth.

## License

To be determined before the first public release.
