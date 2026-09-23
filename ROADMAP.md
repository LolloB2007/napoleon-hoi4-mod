# Napoleonic Era: development roadmap

**Current branch: Milestone 4: coalition rounds, funding, separate peace and treaty safety**

Implementation, static verification and successful in-game testing are separate statuses. A PR does not complete an engine acceptance test merely by adding files.

| Milestone | Current status |
|---|---|
| 1 | Country setup exists; engine verification pending |
| 2 | Opening wars retain their starting structure; treaty effects now idempotent and ownership-guarded; engine verification pending |
| 3 | Partial: 450 French focuses, 84 policy events and 56 chapter spirits; bespoke campaigns and approved territorial policy remain |
| 4 | Partial: seven shared-framework coalition rounds, consent invitations, 12 subsidies, 13 peace requests and guarded settlement; bespoke treaties and fallback leadership remain |
| 5 | Existing major-power trees; deep-content pass pending |
| 6 | Partial: eight bounded meters, twelve decisions, eleven spirits and battle/peace/occupation pulses; deeper politics pending |
| 7 | Blocked on representative in-game campaign measurements |
| 8 | Country setup only; deep campaigns and formables pending |
| 9 | Placeholders only; legacy localisation, presentation and rights review pending |

All original detailed milestone checklists and chronological phases are retained in [the milestone catalogue](docs/roadmap-milestones.md). This file is the current status authority; historic checkmarks in the catalogue are not runtime certification.

## Authorized end-product requirements

- [ ] At least **450 distinct French focuses** across the existing and subsequently approved routes.
- [ ] Varied focus lengths, meaningful branching and route-safe outcomes.
- [ ] Substantial events and decisions with consequences, not repeated filler rewards.
- [ ] Earned integration of eligible territory, with the catalogue approved under A04.
- [ ] Formables, releasables, client relationships and faction dynamics.
- [ ] A coherent, tested 1789-1795 slice before full-campaign acceptance.

## Delivered on this branch

- 450 French focus definitions and 84 policy events retained
- Eight reusable state/army meters and twelve management decisions
- Seven coalition rounds with native temporary factions and voluntary entry
- Twelve funded subsidies and thirteen negotiated peace requests
- Settlement locks, re-entry cooldowns, own-faction checks and third-party territory protection
- Opening treaties execute immediately rather than waiting for player acknowledgement
- Jassy uses valid state-scoped core edits and cannot seize third-party Odessa
- Tracking documents updated; alternate-winner treaty terms and territorial approvals remain open

## Test evidence and remaining acceptance

72 local unit tests pass. Coalition integration uses local fixtures, while the CI generator also reads exact retained master blobs. Tests cover ordering, payment conservation, consent checks, bounded/idempotent settlement, scope conventions and output path safety. No HOI4 runtime test has been performed; simultaneous-war and faction behavior remains an engine acceptance item.

- [ ] Fresh game on the approved engine/DLC baseline.
- [ ] Save/reload and AI-only campaign.
- [ ] Both sides of every limited war; no unintended peace conference or annexation.
- [ ] No repeated reward, deleted third-party country, or cross-route event.
- [ ] Focus-tree rendering, reachability and visible localisation in game.
- [ ] Campaign measurements before military balance is declared complete.

## Approval and development rules

The queue is [to ask lollo.md](to%20ask%20lollo.md). **Revisit scripted peace deals when the historically losing side wins.** Calendar flexibility, the end date, expansive coring and speculative union borders remain approval-dependent.

Each milestone gets its own PR, even when only an explicitly identified slice is implemented. Dependent PRs may be stacked: merge the parent first, then retarget its child to master. No workflow merges PRs. Every PR keeps README, this roadmap, the approval queue and test evidence current.

Build playable historical slices: **1789-1795 > 1796-1804 > 1805-1807 > 1808-1811 > 1812-1815**. Do not equate generated file counts with finished campaigns.
