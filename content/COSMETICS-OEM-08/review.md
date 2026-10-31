# Render and source review — COSMETICS-OEM-08 / LinkedIn English

## Completed

- English card copy: **10 cards**, source-locked to the user-uploaded Korean article.
- JSON field length and sequence checks: **PASS**, no field over the English caps checked in `docs/card-authoring-spec.md`.
- Content distribution: 1 cover, 1 bars card, 1 process, 3 other comparison/concept cards, 1 rest, 1 flow, 1 table, 1 CTA. One message per card.
- Visible copy (headline + body + takeaway + promise where present): approximately **320.2 English characters per card** (counted with spaces), within the cited 280–440 character set target.
- Visual accent: navy/cream alternation and GitHub main brand color tokens; real-ratio bars 1,000 / 900 / 400; 1 rest slide; 4 takeaway bars, at the 40% maximum.
- Local render: **PASS** for 10 PNG files at 1080 × 1350, 10-page PDF at 540 × 675 PDF points, and generated 2-up/4-up review sheets.
- Programmatic layout check: **72** measured text blocks, **0 declared overflows**, followed by visual review of the overview sheet and cards 09 and 10.
- Source claim check: order vs production vs sales, 2026 production versus 2027 receipt, February 2027 production-report deadline, manager training, regular/rapid safety reports, limited self-made soap exception, and free vs paid boundary retained from source.
- Icon names in JSON were checked against GitHub's vendored Lucide SVG filenames.

## Not completed / not claimed

- **User approval of the article / card copy:** not explicitly confirmed; `approvedBy` remains a draft marker.
- **Independent legal-update verification:** not performed; this is a transformation of the user-provided source, not a newly researched legal memorandum. `factCheck` remains `pending`.
- **Official Ethos renderer and official QA:** repository checkout and its `scripts/qa_render.py`, `scripts/copy_lint.py`, `scripts/design_review.py` were unavailable in this environment. The output was created with a deterministic **local Pillow preview renderer**, not the GitHub HTML/Chromium pipeline. Do not report official QA PASS.
- **Exact brand font conformity:** GitHub `brand/tokens.json` colors and 4:5 geometry were matched, but local Inter fonts were substituted for the repository's required ETHOS font assets. Official typography/font-load QA remains pending.
- **Human publication sign-off:** not performed. This preview should not be described as approved or published.

## Human checks before publishing

1. Recheck the user-supplied Korean source's legal conditions and any intervening amendments against official texts and the operating year.
2. Review especially the limited soap exception on card 09, the two report clocks on card 08 and the free/paid boundary on card 10.
3. Run the repository renderer/QA for brand font parity after merging or in CI, inspect the true output sheet and approve the final published copy separately.