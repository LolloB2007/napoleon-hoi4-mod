# Suggestions

**Current as of 23 September 2026.** These are forward-looking proposals based on the merged `master` state after PR #25. They are not approvals. A01-A12, the current focus-count targets and the explicit formable-core policy are already implemented and should not be re-proposed as unfinished work.

## Priority 1 — Prove the current build in HOI4

| Proposal | Why it matters | Concrete acceptance target |
|---|---|---|
| 1789–1795 engine acceptance pass | Static tests cannot catch scope errors, invalid modifiers, UI failures or engine-only event behaviour | Fresh start, save/reload, five-year observer run, no recurring error-log spam, no broken starting wars |
| Full-campaign observer runs | The mod now has enough content that AI sequencing and late-game state are the main unknowns | Observer campaigns through 1805, 1812 and post-1815 with recorded failures and state snapshots |
| Focus-tree usability audit | 4,000+ focus nodes can be valid script and still be miserable to navigate | Check clipping, line routing, branch visibility, unreachable nodes, AI availability and player readability for every campaign |
| Save-compatibility smoke tests | Large generated trees and state variables can fail only after reload | Save/reload at Revolution, coalition war, formable creation and late campaign; compare flags/variables before and after |

## Priority 2 — Replace breadth with bespoke historical depth

The mod has enough focus nodes. **Do not solve the next quality problems by adding another thousand generic focuses.** Use events, decisions, variables, characters, scripted peace and campaign-specific mechanics.

### France

- Turn the Revolution into a real political crisis system: Estates-General, Assembly/Convention transitions, Jacobin–Girondin struggle, Vendée, assignats, Committee of Public Safety, Terror and Thermidor.
- Give Napoleon's rise bespoke mechanics for the Italian Campaign, Egypt, prestige, Brumaire, Consulate, coronation and Marshals rather than relying mostly on focus completion.
- Build the Continental System as an actual enforcement/evasion mechanic affecting subjects, allies, neutrals and British trade.
- Make the Peninsular War a sustained occupation/guerrilla problem rather than a normal front.
- Make the 1812 campaign about preparation, depots, attrition, retreat and army collapse, with meaningful outcomes short of scripted historical defeat.
- Give 1814, the Restoration, Hundred Days and the postwar settlement proper state transitions.

### Britain, Austria, Prussia and Russia

The focus counts are already in the requested 350–400 range. The next pass should make their campaigns **feel unlike one another**:

- **Britain:** parliamentary politics, credit/subsidy capacity, Royal Navy blockade, colonial commitments, Peninsular intervention and industrialisation.
- **Austria:** Josephine legacy, Belgian unrest, Archduke Charles, HRE crisis, dynastic federalism, Austrian Empire formation and postwar diplomacy.
- **Prussia:** conservative stagnation, Jena catastrophe, Stein–Hardenberg/Scharnhorst reform, Landwehr, liberation and the German leadership question.
- **Russia:** Catherine/Paul/Alexander succession, partitions, Speransky, Ottoman/Swedish frontiers, 1812 strategic withdrawal and the Holy Alliance.

The 324-focus deep-programme layers should be treated as campaign scaffolding. Over time, replace the most generic stretches with bespoke crises and decision systems rather than increasing the raw count further.

### Secondary countries

Every secondary campaign already has an effective 175 focuses and at least 38 country-specific focuses. The next improvement is **personalised event and decision content**, not more nodes.

Priorities:
- 3–5 bespoke multi-event crisis chains per campaign.
- Country-specific military or constitutional mechanic where historically justified.
- Dynamic regime-transition events for WAR, BAT and HOL.
- Distinct diplomatic mechanics for the seven German principalities rather than only shared regional systems.
- More country-specific AI priorities so 175-focus trees do not all progress with the same rhythm.

## Priority 3 — Finish coalition and peace gameplay

- Add fallback coalition leadership when Britain is unavailable, defeated or politically unsuitable.
- Expand coalition eligibility from round sequencing into threat, French expansion, client-state and ideological reaction.
- Give each major coalition war a bounded **war-objective catalogue** so peace terms reflect who won and what was contested.
- Add more separate-peace cases for exhausted minor participants without collapsing the whole coalition.
- Make British subsidies depend on treasury/credit and strategic priority rather than being a generic support button.
- Audit every scripted peace for third-party ownership, dead tags, subject states and repeated callbacks.
- Test both victor directions for every limited opening war and representative coalition war.

## Priority 4 — Reconstruct the 1789 world more precisely

### Starting armies and OOBs

`history/units/` still contains the secondary-country OOBs but no checked-in `FRA_1789`, `ENG_1789`, `HAB_1789`, `PRU_1789` or `RUS_1789` files. Resolve the major-power starting OOB contract before declaring the 1789 start complete.

Recommended next step:
- Build explicit 1789 OOB files for all five majors.
- Validate deployed templates, equipment pools, commander assignment and fleet composition in-engine.
- Keep corps/division scale consistent with the mod's combat model instead of reproducing historical regiment counts literally.

### Map and overseas scope

A07 already defines the intended scope. The missing work is implementation accuracy:
- Audit 1.19.x state IDs before changing ownership.
- Reconstruct relevant European possessions, North Africa, Canada/USA, India and the necessary colonial theatres.
- Remove remaining 1936 ownership/core artefacts in approved-scope regions.
- Do not invent detailed ownership for out-of-scope regions merely to fill the map.

## Priority 5 — Balance with evidence

Milestone 7 should now become empirical.

Create repeatable campaign fixtures for:
- Revolutionary Wars / First Coalition.
- 1805.
- 1806 Prussia.
- Peninsular War.
- 1812 Russia.
- 1813–1814.
- Waterloo/Hundred Days.

Record at minimum:
- army size and manpower,
- equipment deficits,
- organisation/recovery,
- battle casualties,
- attrition,
- supply status,
- war exhaustion,
- treasury/debt,
- campaign duration,
- AI front behaviour.

Balance objectives:
- Battles should normally break cohesion faster than annihilate whole armies.
- Cavalry should matter most in mobility, shock and exploitation without becoming universal super-infantry.
- Siege artillery should be strategically valuable and operationally cumbersome.
- Long campaigns should fail through supply, attrition, exhaustion and political strain as well as battlefield defeat.

## Priority 6 — AI and pacing

- Add route-aware AI plans for France's four political outcomes.
- Give each major an explicit historical priority sequence plus bounded alternate-route weights.
- Prevent AI from pursuing every available deep programme simply because it exists.
- Use completion gates and mutually exclusive programme groups to create recognizable campaign phases.
- Check whether 175-focus secondary trees cause AI paralysis, random-walk focus selection or excessive delayed military preparation.
- Add AI-specific sanity tests for coalition entry, formables, client restoration and territorial integration.

## Priority 7 — Performance and repository engineering

The content compiler is now processing thousands of focus definitions and a large presentation layer. Improve iteration speed before the repository becomes its own weather system.

- Cache generated presentation textures by seed and dimensions.
- Avoid reparsing unchanged generated focus trees during presentation post-processing where possible.
- Extend the generated manifest to record **builder/source ownership**, not only content hashes.
- Add a fast test mode that skips binary presentation generation for logic-only CI jobs.
- Keep one full generation/presentation job as the release-quality gate.
- Add explicit focus-count and branch-visibility summaries to generated docs so regressions are immediately visible.
- Keep `content/status.json`, `ROADMAP.md` and generated docs synchronized with merged `master`, not the name of a now-deleted development branch.

## Priority 8 — Presentation follow-up

A10-A12 are already implemented. Improvements from here should be quality upgrades, not another policy decision.

- Replace only the most visible procedural portraits/event scenes with rights-cleared or original human-authored flagship art.
- Expand the soundtrack gradually with original compositions and newly recorded/rendered public-domain repertoire; keep recording provenance separate from composition provenance.
- Give major campaign mechanics bespoke UI panels only where ordinary decisions/events become hard to understand.
- Improve focus-tree navigation with section labels, spacing and visual hierarchy before adding more focus nodes.
- Keep strategic-map changes understated unless a tested map treatment materially improves readability.

## Things not to re-propose

These are already decided or implemented unless a new owner decision explicitly changes them:

- A01 historical dates as minimum focus gates.
- A02 open-ended campaign.
- A03 outcome-aware bounded peace.
- A04 restrictive historical/formable coring.
- A05 audited formables.
- A06 normal puppet relationships for clients.
- A07 approved geographic scope.
- A08 HOI4 1.19.x + La Résistance baseline.
- A09 plausible near-counterfactual alternate-history limits.
- A10 painted/engraved/cartographic presentation direction.
- A11 original + newly rendered public-domain soundtrack policy.
- A12 English-only maintained localisation.
- France target of roughly 600–650 focuses.
- Other-major target of roughly 350–400 focuses.
- Secondary-country target of roughly 150–200 focuses with at least 30–40 personalised focuses.
- Formables granting cores from explicit audited `core_states` catalogues.

## Recommended next development sequence

1. **1789–1795 runtime certification and major OOB repair.**
2. **Early French Revolution bespoke mechanics and First Coalition gameplay.**
3. **AI/focus-tree pacing pass across the newly expanded campaigns.**
4. **Military balance fixtures and evidence collection.**
5. **1796–1804 bespoke France + major-power crisis content.**
6. **1805–1815 coalition, Peninsular, Russian-campaign and collapse mechanics.**
7. **Presentation replacement/polish only after the gameplay slices are stable.**

The repository now has enough breadth. The next gains come from **engine proof, bespoke mechanics, AI quality and campaign balance**, not raw file or focus counts.
