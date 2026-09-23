# Napoleonic Era: development roadmap

**Current status: Milestone 9 merged; A01–A12 approved; next step is implementation of the owner decisions**

Implementation, static verification and successful in-game testing are separate statuses. A PR does not complete an engine acceptance test merely by adding files.

| Milestone | Current status |
|---|---|
| 1 | Country setup exists; four great-power rulers corrected; engine verification pending |
| 2 | Opening diplomacy and bounded treaties implemented; engine verification pending |
| 3 | Partial: 450 French focuses, 84 policy events and 56 chapter spirits; deeper bespoke campaigns remain |
| 4 | Partial: seven coalition rounds, consent, funding and separate peace; bespoke treaties and fallback leadership remain |
| 5 | Partial: 108 new great-power focuses, 24 policy reviews, 12 spirits and starting-leader/succession repairs |
| 6 | Partial: eight bounded state/army meters, twelve paid decisions, eleven spirits and campaign pulses |
| 7 | Campaign measurement infrastructure pending; actual balance requires in-game evidence |
| 8 | Implementation complete: territorial/client foundation plus 13 secondary campaign packs; runtime validation pending |
| 9 | Non-gated implementation complete and merged. A10 visual direction, A11 soundtrack direction and A12 translation scope are now approved; implementation of those final choices is the next pass. |

All original detailed milestone checklists and chronological phases are retained in [the milestone catalogue](docs/roadmap-milestones.md). This file is the current status authority; historic checkmarks in the catalogue are not runtime certification.

## Next development pass — implement approved owner decisions

The immediate next step is to implement the decisions recorded under **A01–A12** in [to ask lollo.md](to%20ask%20lollo.md).

Priority work:

- [ ] Convert historical focus dates to **minimum-date focus gates only**; remove exact-date forcing from unrelated systems.
- [ ] Remove the hard practical campaign end date.
- [ ] Expand bounded scripted peace logic so the actual victor receives a war-appropriate settlement, including non-historical winners.
- [ ] Enforce historical/formable-only coring and add approved targeted compliance bonuses instead of conquest cores.
- [ ] Implement the conventional + limited credible alternate-history formable catalogue with explicit founders and borders.
- [ ] Standardize client/releasable mechanics around HOI4 puppet relationships.
- [ ] Expand the world scope to European states, European colonial possessions, North Africa, USA, Canada and India while leaving irrelevant regions impassable/inert where appropriate.
- [ ] Declare **La Résistance** as required and keep the runtime target on HOI4 1.19.x.
- [ ] Expand plausible alternate political/dynastic routes without meme paths.
- [ ] Move presentation toward the approved painted/engraved/cartographic hybrid aesthetic with asset provenance.
- [ ] Build a soundtrack from original scoring plus newly rendered public-domain Revolutionary/Napoleonic repertoire.
- [ ] Keep English as the only maintained localisation for now.

This pass should be broken into reviewable PRs where the implementation areas are logically separable. Owner approval is no longer required for work that stays within these rules.

## Authorized end-product requirements

- [ ] At least **450 distinct French focuses** across the existing and subsequently approved routes.
- [ ] Varied focus lengths, meaningful branching and route-safe outcomes.
- [ ] Substantial events and decisions with consequences, not repeated filler rewards.
- [ ] Earned integration of eligible territory, with the catalogue approved under A04.
- [ ] Formables, releasables, client relationships and faction dynamics.
- [ ] A coherent, tested 1789-1795 slice before full-campaign acceptance.

## Delivered on this branch

- 450 French focus definitions, 108 additional great-power focuses and 299 secondary-power focuses
- Reusable era mechanics and seven temporary coalition rounds
- Territorial/client foundation with approval-gated integration and formable registries
- Thirteen secondary campaign packs covering every Milestone 8 geography
- A deterministic original focus icon for every current focus ID and period-styled pictures for every scripted event
- Original portrait cards wired to current inline political leaders, marshals, generals and admirals
- Default plus four regime-specific generated flags across the 68-tag namespace
- Three original loading screens, refreshed 1789 bookmark artwork and common Napoleonic UI ornaments
- Original event stingers, twelve additional flavour events, historical corps/division naming groups and sailing-warship names
- English localisation cleanup removing obvious generator/temporary language and normalising terminology
- Asset-provenance documentation with no external commercial imagery, recordings or font files

## Test evidence and remaining acceptance

Milestone 9 adds presentation tests for focus-icon coverage, event pictures, leader portraits, regime flags, loading/bookmark formats, event audio, flavour events, historical namelists, OOB naming integration, English localisation cleanup and asset provenance. GitHub Actions must still pass, and no HOI4 executable was run.

- [ ] Fresh game on the approved engine/DLC baseline.
- [ ] Save/reload and AI-only campaign.
- [ ] Both sides of every limited war; no unintended peace conference or annexation.
- [ ] No repeated reward, deleted third-party country, or cross-route event.
- [ ] Focus-tree rendering, reachability and visible localisation in game.
- [ ] Campaign measurements before military balance is declared complete.

## Approval and development rules

The approval record is [to ask lollo.md](to%20ask%20lollo.md). **A01–A12 are now approved and define the next implementation pass.** Scripted peace deals must produce bounded outcomes appropriate to the actual victor; historical treaties must not be forced when the opposite side wins.

Each milestone gets its own PR, even when only an explicitly identified slice is implemented. Dependent PRs may be stacked: merge the parent first, then retarget its child to master. No workflow merges PRs. Every PR keeps README, this roadmap, the approval queue and test evidence current.

Build playable historical slices: **1789-1795 > 1796-1804 > 1805-1807 > 1808-1811 > 1812-1815**. Do not equate generated file counts with finished campaigns.
