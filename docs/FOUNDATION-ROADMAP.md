# Foundation Roadmap

This is the build order for the first stable architecture. It is intentionally ordered so that later features have something solid underneath them.

## Phase 0 — Foundation

- [x] Repository established
- [x] Architecture boundary documented
- [x] Canonical NTX document policy established
- [x] External format roles established
- [ ] Python package skeleton
- [ ] NTX domain model
- [ ] Diagnostics model
- [ ] Versioning policy implemented
- [ ] CI and formatting/linting/test baseline

## Phase 1 — Musical core

- [ ] Pitch representation
- [ ] Duration/time-position representation
- [ ] Meter and key signatures
- [ ] Clefs and written/concert pitch context
- [ ] Parts, staves, voices, measures
- [ ] Notes, rests, chords
- [ ] Ties, tuplets, beams
- [ ] Basic articulations/dynamics
- [ ] Provenance and uncertainty primitives
- [ ] Canonical JSON serialization

## Phase 2 — Transposition

- [ ] Pitch transposition engine
- [ ] Key-signature transposition
- [ ] Enharmonic spelling policy
- [ ] Written vs concert pitch handling
- [ ] Clef-aware presentation changes
- [ ] Deterministic transformation reports
- [ ] Semantic regression corpus

## Phase 3 — Interchange

- [ ] MusicXML 4.0 import
- [ ] MusicXML 4.0 export
- [ ] MusicXML round-trip fixtures
- [ ] MEI import
- [ ] MEI export
- [ ] ABC import/export
- [ ] Loss/provenance reporting

## Phase 4 — Tablature

- [ ] First-class tuning model
- [ ] String/course/fret representation
- [ ] Tab parsing grammar
- [ ] Staff → tab candidate generation
- [ ] Tab → pitched notation mapping
- [ ] Candidate ranking policies
- [ ] Explicit ambiguity reporting
- [ ] Guitar/bass-oriented fixtures

## Phase 5 — Presentation

- [ ] TUI inspection view
- [ ] Before/after transformation view
- [ ] Diagnostics browser
- [ ] Provenance browser
- [ ] Tab/staff comparison view
- [ ] Renderer adapter boundary

## Phase 6 — Recognition

Only after the deterministic core is trustworthy:

- [ ] PDF/image ingestion boundary
- [ ] Recognition result schema
- [ ] Confidence representation
- [ ] Candidate alternatives
- [ ] Human verification workflow
- [ ] Golden scan corpus

Recognition is deliberately later. We do not want an uncertain OCR system defining the semantics of the rest of the project.

## Phase 7 — Advanced transformation

Potential future work:

- instrument-aware rewriting
- alternate tunings
- capo-aware realization
- fingering optimization
- voice separation
- rhythmic reconstruction
- notation cleanup/normalization
- comparative score analysis
- additional notation formats

These are not architecture commitments until their requirements are understood.
