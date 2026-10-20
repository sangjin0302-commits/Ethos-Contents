# Card design and writing workflow — 2026-10-20

Base: `f45ea9434fc12c55a33dbc0d9df51f4f130f13a9`. User-authorized code, instruction and layout improvements; no publication or new legal claims.

## Preservation

- OEM `blog.md` and both `card-data` files are unchanged against the base commit.
- All 20 Korean/English HTML copy blocks before the fitting script are identical to the base. HTML changes replace only font fitting; layout changes live in `design.css`.
- Historical language-method records remain supported without migration. Applying prose suggestions invalidates approval and resets review stages.
- Legacy deterministic sets still rebuild identically.

## Changes

- CI keeps design warnings advisory; hard QA and fallback-production failures remain blocking.
- Design and copy checkers no longer prescribe icon quotas. Repeated layouts can remain when they explain related information.
- Both bar renderers preserve actual proportions, including zero and tiny values. Negative/nonfinite values fail.
- Explicit cover style overrides fallback selection; issue parity no longer changes it. Panel illustrations are honored.
- Unordered lists do not acquire step numbers. Explicit numbering and actual processes remain supported.
- Production measures overflow without resizing text. Preview fitting is capped at 8% and reported.
- `writing_context.py` retrieves exact, relevant user-edit examples. The real polish payload and `--print-request` include the same examples. They are read-only style context, never factual evidence for a new manuscript.
- Blog guidance checks argument flow and redundant explanations before local polishing. Card guidance permits evidence/comparison/rest cards without forced Q&A. Redundant takeaways may be omitted in new drafts, never silently deleted from approved copy.
- New review records separate completion status and method; legacy records remain valid.

## Visual inspection

Opened both freshly rendered 270px sheets and full-size Korean/English card 7.

- Cards 3/7 use open full-width rows. Korean condition text is 22 CSS px; English condition text is 21 CSS px.
- Card 7 retains duty, exception factors and confidentiality boundary. English exception factors remain separate lines.
- Checklists 4/9 use neutral markers; procedure card 5 keeps its sequence.
- Closing text is 19 CSS px. All 20 cards have fitScale 1.00 and no fit overflow.
- Card 8 intentionally pauses with a large sentence and open space. Its balance/empty-band warnings are accepted without adding filler.
- Legal-density warnings remain on card 7 and English CTA. Approved conditions take precedence over advisory character counts.

## Validation

- Final pytest result is recorded in the companion OEM `review.md`.
- Guideline validation: 46 manifest paths passed; reusable card smoke passed.
- Visual regression: all five baseline images unchanged, 0.000% difference. No baseline/threshold relaxation.
- Stress render: 14 card configurations and eight OG configurations passed.
- Final OEM render: 10 Korean and 10 English cards passed hard QA and produced PNGs.
- Source comparison and copy-lock checks passed.

Restricted browser execution stalled; local browser checks succeeded outside the sandbox. No paid language-model API was called. This does not constitute new legal verification or publication approval.
