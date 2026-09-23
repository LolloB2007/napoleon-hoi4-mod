# Napoleonic Era: development roadmap

**Current branch: Milestone 8 complete: secondary-power campaigns and territorial/client framework**

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
| 8 | Implementation complete: territorial/client foundation plus 13 secondary campaign packs covering every roadmap geography; runtime validation pending |
| 9 | Placeholder assets only; legacy localisation and presentation review pending |

All original detailed milestone checklists and chronological phases are retained in [the milestone catalogue](docs/roadmap-milestones.md). This file is the current status authority; historic checkmarks in the catalogue are not runtime certification.

## Authorized end-product requirements

- [ ] At least **450 distinct French focuses** across the existing and subsequently approved routes.
- [ ] Varied focus lengths, meaningful branching and route-safe outcomes.
- [ ] Substantial events and decisions with consequences, not repeated filler rewards.
- [ ] Earned integration of eligible territory, with the catalogue approved under A04.
- [ ] Formables, releasables, client relationships and faction dynamics.
- [ ] A coherent, tested 1789-1795 slice before full-campaign acceptance.

## Delivered on this branch

- 450 French focus definitions, 108 additional great-power focuses and their policy events
- Reusable era mechanics and seven temporary coalition rounds
- Sixteen peaceful independent-release decisions and twelve client-aid decisions
- Approval-gated integration/formable registry and consent-based Rhine client charters
- Thirteen secondary campaign packs covering Spain, Poland/Warsaw, the Ottoman Empire, Sweden, five Italian states, German principalities, Portugal, the Netherlands and the United States
- 299 secondary focuses, 52 secondary events, 39 recurring decisions and 65 campaign spirits
- Historical and bounded alternate routes, military-development branches, major-power diplomatic links and localisation for every Milestone 8 campaign family
- Dynamic WAR, BAT and HOL tags inherit the Polish or Dutch campaign; USA, Baden, Hesse and Mecklenburg receive missing political-character baselines

## Test evidence and remaining acceptance

The suite adds 14 dedicated Milestone 8 tests on top of the existing 104-test baseline. It checks campaign coverage, 299 unique focus IDs, route exclusivity, 52 unique events, 39 decisions, 65 spirits, localisation, dynamic-tag inheritance, bounded great-power links, USA baseline data and absence of unapproved territorial effects. GitHub Actions must still pass, and no HOI4 executable was run.

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
