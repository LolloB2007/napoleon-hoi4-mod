# Napoleonic Era: development roadmap

**Current branch: Milestone 6: reusable state and army management slice**

Implementation, static verification and successful in-game testing are separate statuses. A PR does not complete an engine acceptance test merely by adding files.

| Milestone | Current status |
|---|---|
| 1 | Country setup exists; engine verification pending |
| 2 | Opening wars and bounded treaties exist; engine verification pending |
| 3 | 29 existing French focuses; expansion target at least 450 |
| 4 | Not implemented beyond opening-war diplomacy |
| 5 | Existing major-power trees; deep-content pass pending |
| 6 | Partial: eight bounded meters, twelve decisions, eleven spirits and battle/peace/occupation pulses; deeper state and client politics pending |
| 7 | Blocked on representative in-game campaign measurements |
| 8 | Country setup only; deep campaigns and formables pending |
| 9 | Placeholder assets only; presentation and rights review pending |

All original detailed milestone checklists and chronological phases are retained in [the milestone catalogue](docs/roadmap-milestones.md). This file is the current status authority; historic checkmarks in the catalogue are not runtime certification.

## Authorized end-product requirements

- [ ] At least **450 distinct French focuses** across the existing and subsequently approved routes.
- [ ] Varied focus lengths, meaningful branching and route-safe outcomes.
- [ ] Substantial events and decisions with consequences, not repeated filler rewards.
- [ ] Earned integration of eligible territory, with the catalogue approved under A04.
- [ ] Formables, releasables, client relationships and faction dynamics.
- [ ] A coherent, tested 1789-1795 slice before full-campaign acceptance.

## Delivered on this branch

- 68-country source namespace, placeholder flags and build validation
- Eight bounded treasury/debt/legitimacy/fervor/exhaustion/prestige/reform/supply meters
- Twelve paid decisions with explicit resource requirements and cooldowns
- Eleven threshold or temporary national spirits
- Country-scoped monthly processing and national army prestige from battle hooks
- Read-only drift verification and synchronized approval/roadmap/readme documents

## Test evidence and remaining acceptance

26 local unit tests pass, covering syntax, resources, route gates, bounds and non-quadratic monthly processing. The reference model is not an engine emulator. No HOI4 process was executed.

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
