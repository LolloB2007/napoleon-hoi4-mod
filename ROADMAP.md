# Napoleonic Era: development roadmap

**Current branch: Milestone 5: distinct great-power programmes and starting-leader correction**

Implementation, static verification and successful in-game testing are separate statuses. A PR does not complete an engine acceptance test merely by adding files.

| Milestone | Current status |
|---|---|
| 1 | Country setup exists; four great-power starting rulers corrected; engine verification pending |
| 2 | Opening diplomacy and bounded treaties implemented; engine verification pending |
| 3 | Partial: 450 French focuses, 84 policy events and 56 chapter spirits; deeper campaigns and territorial policy remain |
| 4 | Partial: seven coalition rounds, consent, funding, separate peace and guarded treaties; bespoke settlements and fallback leadership remain |
| 5 | Partial: 108 new focuses, 24 policy reviews, 12 spirits, three guarded successions and starting-leader fixes; full country campaigns remain |
| 6 | Partial: eight bounded meters, twelve decisions, eleven spirits and campaign pulses |
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

- French 450-focus expansion and reusable era mechanics retained
- Seven shared-framework coalition rounds with paid subsidies and bounded peace
- Britain: parliamentary credit, maritime policy and sustainable allied finance
- Austria: provincial institutions, field-command reform and the dynastic network
- Prussia: state institutions, army reform and mobilization/recovery
- Russia: provincial administration, long-distance armies and ministerial reform
- Four starting histories no longer create later rulers immediately
- Three succession events check the previous reigning monarch; Russian succession focuses create their named leaders
- README, roadmap, approval queue and suggestions synchronized

## Test evidence and remaining acceptance

86 local unit tests pass. Great-power tests cover 108 unique focus names, reference graphs, policy payment/credit limits, safe deferral, four starting rulers, guarded succession and localisation. Exact retained repository sources are also built by CI. No HOI4 process was run; these are substantial implementation slices, not certified full campaigns.

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
