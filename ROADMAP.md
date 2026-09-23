# Napoleonic Era: development roadmap

**Current branch: A01-A12 implemented in the stacked approval series; static validation and HOI4 runtime certification remain**

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
| 9 | Implementation complete for approved A10-A12 direction: painted/engraved/cartographic presentation, provenance-tracked soundtrack seed, and enforced English-only localisation. Runtime validation pending. |

All original detailed milestone checklists and chronological phases are retained in [the milestone catalogue](docs/roadmap-milestones.md). This file is the current status authority; historic checkmarks in the catalogue are not runtime certification.

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
- A10 hybrid painted/engraved/cartographic presentation direction
- A11 HOI4 music registration with original scoring and a newly rendered public-domain period composition
- A12 enforced English-only maintained localisation policy

## Test evidence and remaining acceptance

A01-A12 add regression coverage for chronology gates, open-ended campaign, outcome-aware settlements, coring/formables/clients, geographic scope, DLC baseline, alternate-route plausibility, presentation, music provenance, and English-only localisation. GitHub Actions and a real HOI4 1.19.x + La Résistance launch remain the final certification gates.

- [ ] Fresh game on the approved engine/DLC baseline.
- [ ] Save/reload and AI-only campaign.
- [ ] Both sides of every limited war; no unintended peace conference or annexation.
- [ ] No repeated reward, deleted third-party country, or cross-route event.
- [ ] Focus-tree rendering, reachability and visible localisation in game.
- [ ] Campaign measurements before military balance is declared complete.

## Approval and development rules

The queue is [to ask lollo.md](to%20ask%20lollo.md). **Revisit scripted peace deals when the historically losing side wins.** A01-A12 are approved implementation policy. New decisions that materially change them require a new owner entry.

Each milestone gets its own PR, even when only an explicitly identified slice is implemented. Dependent PRs may be stacked: merge the parent first, then retarget its child to master. No workflow merges PRs. Every PR keeps README, this roadmap, the approval queue and test evidence current.

Build playable historical slices: **1789-1795 > 1796-1804 > 1805-1807 > 1808-1811 > 1812-1815**. Do not equate generated file counts with finished campaigns.
