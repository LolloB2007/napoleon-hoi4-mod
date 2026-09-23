# Napoleonic Era: development roadmap

**Current branch: Milestone 8: releases, client aid and approval-gated territorial interfaces**

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
| 8 | Partial: 16 releases, 12 client-aid decisions and Rhine consent; integration/formable interfaces implemented but territorial proposals disabled pending approval; deep secondary campaigns remain |
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
- Sixteen peaceful independent-release decisions using existing owned cores only
- Twelve paid client-aid transfers with subject and treasury-cap checks
- Rhine clients now accept or refuse a charter instead of becoming unconditional puppets
- Three French diplomatic paths use guarded native faction templates
- Paid continuous integration and cosmetic-formable generators, disabled by default until borders and approvals are recorded
- Actual integration and formable proposals appended to the approval queue

## Test evidence and remaining acceptance

104 local unit tests pass, including default-disabled approval gates, rejection of empty/duplicate/unattributed borders, continuous integration, safe releases, subject-only aid, faction preservation and Rhine consent. Integration tests use explicitly approved synthetic fixtures, not approval of live maps. No HOI4 runtime test was performed.

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
