# Napoleonic Era: development roadmap

**Current branch: Deep focus expansion implemented on development branch; static and HOI4 runtime validation pending**

Implementation, static verification and successful in-game testing are separate statuses. A PR does not complete an engine acceptance test merely by adding files.

| Milestone | Current status |
|---|---|
| 1 | Country setup exists; four great-power rulers corrected; engine verification pending |
| 2 | Opening diplomacy and bounded treaties implemented; engine verification pending |
| 3 | Partial: 630 French focuses, 120 policy events and 80 chapter spirits; deep campaign runtime validation remains |
| 4 | Partial: seven coalition rounds, consent, funding and separate peace; bespoke treaties and fallback leadership remain |
| 5 | Partial: Britain and Austria target 368 focuses each, Prussia 364 and Russia 366; runtime pacing and bespoke crisis validation remain |
| 6 | Partial: eight bounded state/army meters, twelve paid decisions, eleven spirits and campaign pulses |
| 7 | Campaign measurement infrastructure pending; actual balance requires in-game evidence |
| 8 | Implementation complete in source: 13 secondary campaigns target 175 focuses each, including 38 personalised focuses per campaign; runtime validation pending |
| 9 | Implementation complete for approved A10-A12 direction: painted/engraved/cartographic presentation, provenance-tracked soundtrack seed, and enforced English-only localisation. Runtime validation pending. |

All original detailed milestone checklists and chronological phases are retained in [the milestone catalogue](docs/roadmap-milestones.md). This file is the current status authority; historic checkmarks in the catalogue are not runtime certification.

## Authorized end-product requirements

- [x] France in the **600-650 focus** range (implemented target: 630).
- [x] Britain, Austria, Prussia and Russia in the **350-400 focus** range.
- [x] Each secondary campaign with content in the **150-200 focus** range, including at least 30-40 country-specific focuses.
- [ ] Varied focus lengths, meaningful branching and route-safe outcomes.
- [ ] Substantial events and decisions with consequences, not repeated filler rewards.
- [ ] Earned integration of eligible territory, with the catalogue approved under A04.
- [ ] Formables, releasables, client relationships and faction dynamics.
- [ ] A coherent, tested 1789-1795 slice before full-campaign acceptance.

## Delivered on this branch

- 630 French focuses; Britain 368, Austria 368, Prussia 364 and Russia 366 estimated total focuses; thirteen secondary campaigns at 175 focuses each
- Reusable era mechanics and seven temporary coalition rounds
- Formables grant cores only from explicit audited core-state catalogues on successful formation
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

Deep expansion regression coverage checks France at 630 focuses, each major in the 350-400 range, each secondary campaign at 175 focuses with 38 personalised focuses, explicit formable core sets, syntax, localisation and territorial safety. GitHub Actions and a real HOI4 1.19.x + La Résistance launch remain the final certification gates.

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
