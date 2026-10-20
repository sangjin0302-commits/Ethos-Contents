# Remote CI follow-up and measured changes

Reference date: 2026-10-20. Baseline `f45ea943`; implementation `779d5c7`.
Raw browser measurements: [change-metrics.json](2026-10-20-change-metrics.json).

## Remote findings

- Card system regression and prose hints passed on `779d5c7`.
- Render cards reported success, but its changed-set selector only recognized JSON filenames. HTML/CSS-only changes silently selected zero sets. The selector now includes changes inside existing card sets, including HTML, CSS, blog and terms. Removed/non-card folders remain excluded. Regression tests cover these cases.
- Link integrity failed on two occurrences of the same OASIS research URL. The remote log reports an expired TLS certificate. The previous baseline run failed too. Both www and bare-host HTTPS checks reproduce the certificate failure locally.
- No source URL was replaced with an unrelated source, no HTTP downgrade was made, and TLS checks/exclusions were not relaxed. The external site operator must renew the certificate. This remains an external failure, not a fully green CI result.

## Objective comparison

The baseline was extracted from Git and compared in the same installed Chromium,
540×675 CSS-pixel viewport, device scale factor 2, after fonts loaded.
These are computed CSS sizes, not subjective readability scores.

| Measure | Before | After | Change |
|---|---:|---:|---:|
| Korean card 3 body | 20px | 22px | +10.0% |
| Korean card 7 body | 18px | 22px | +22.2% |
| English card 3 body | 18px | 21px | +16.7% |
| English card 7 body | 21px | 21px | unchanged |
| Korean cards 3/7 closing text | 18px | 19px | +5.6% |
| English cards 3/7 closing text | 17px | 19px | +11.8% |
| Bar length for value 1 against maximum 100 | 7% | 1% | error 6 percentage points → 0 |
| Preview renderer maximum font reduction | 28% | 8% | −20 percentage points |
| New production auto-design font reduction | up to 28% | 0% | removed |
| Collected tests in same environment | 185 | 199 | +14 (+7.6%) |
| Existing blog/card-data files changed | — | 0 | preserved |

The pre-existing QA shrink threshold was already 8%; only the renderer was
inconsistent. Test counts measure coverage volume, not a quality percentage.
The bar comparison is a deterministic renderer reproduction; existing approved
charts were not rewritten. Zero values are now accepted and rendered at zero.

## What has not been demonstrated

- Approved prose was preserved. No reader study or blinded comparison of new
  drafts was conducted; there is no measured percentage gain in naturalness.
- Writing examples now reach the actual polishing request, and structure-first
  guidance is implemented. Paid model execution and reader outcomes remain
  untested.
- Larger text and fewer nested boxes are measurable design changes; preference,
  comprehension, swipe completion and consultation conversion remain unmeasured.
- Dense legal conditions still need editorial judgment. Advisory style warnings
  do not authorize changing approved text.

Next useful evaluation is a separate unapproved draft comparison using the same
source, followed by blind reader preference and comprehension checks. Actual
publication metrics require comparable traffic and a defined observation period.

## Local follow-up validation

- `pytest tests -q`: 199 passed, four dependency deprecation warnings, no skips.
- `ci_render.py --changed f45ea943`: selected COSMETICS-OEM-04; 20 cards and
  two OG images passed. The Korean contact sheet was reopened for visual review.
- Remote `779d5c7` render log explicitly said `no card-data changes to render`
  and uploaded no artifact, confirming the selector regression rather than
  inferring it from a green badge.
