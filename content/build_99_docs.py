"""Generate project-facing documentation from branch status."""
import json


def build(root):
    status = json.loads((root/'content/status.json').read_text())
    table = '\n'.join(f'| {key} | {value} |' for key,value in status['milestones'].items())
    delivered = '\n'.join('- '+item for item in status['delivered'])
    report = status['tests']
    header = f"**Current branch: {status['stage']}**"
    roadmap = f'''# Napoleonic Era: development roadmap

{header}

Implementation, static verification and successful in-game testing are separate statuses. A PR does not complete an engine acceptance test merely by adding files.

| Milestone | Current status |
|---|---|
{table}

All original detailed milestone checklists and chronological phases are retained in [the milestone catalogue](docs/roadmap-milestones.md). This file is the current status authority; historic checkmarks in the catalogue are not runtime certification.

## Authorized end-product requirements

- [x] France in the **600-650 focus** range (implemented target: 630).\n- [x] Britain, Austria, Prussia and Russia in the **350-400 focus** range.\n- [x] Each secondary campaign with content in the **150-200 focus** range, including at least 30-40 country-specific focuses.
- [ ] Varied focus lengths, meaningful branching and route-safe outcomes.
- [ ] Substantial events and decisions with consequences, not repeated filler rewards.
- [ ] Earned integration of eligible territory, with the catalogue approved under A04.
- [ ] Formables, releasables, client relationships and faction dynamics.
- [ ] A coherent, tested 1789-1795 slice before full-campaign acceptance.

## Delivered on this branch

{delivered}

## Test evidence and remaining acceptance

{report}

- [ ] Fresh game on the approved engine/DLC baseline.
- [ ] Save/reload and AI-only campaign.
- [ ] Both sides of every limited war; no unintended peace conference or annexation.
- [ ] No repeated reward, deleted third-party country, or cross-route event.
- [ ] Focus-tree rendering, reachability and visible localisation in game.
- [ ] Campaign measurements before military balance is declared complete.

## Development rules

A01-A12 are established implementation policy. **Revisit scripted peace deals when the historically losing side wins.** New changes that materially alter those policies should be documented explicitly in the relevant design/source file.

Each milestone gets its own PR, even when only an explicitly identified slice is implemented. Dependent PRs may be stacked: merge the parent first, then retarget its child to master. No workflow merges PRs. Every PR keeps the README, roadmap and test evidence current.

Build playable historical slices: **1789-1795 > 1796-1804 > 1805-1807 > 1808-1811 > 1812-1815**. Do not equate generated file counts with finished campaigns.
'''
    readme = '''# Napoleonic Era

**Napoleonic Era** is a Hearts of Iron IV total-conversion project beginning on **5 May 1789**, built around the French Revolution, the Revolutionary Wars and the Napoleonic era.

The campaign is Europe-first, with France as the narrative centre and substantial playable content for Britain, Austria, Prussia, Russia and a broad set of secondary powers.

## What is in the mod

### Major campaigns

- **France:** 630 focuses across constitutional, republican, royalist and Bonapartist paths.
- **Britain:** roughly 368 focuses.
- **Habsburg Austria:** roughly 368 focuses.
- **Prussia:** roughly 364 focuses.
- **Russia:** roughly 366 focuses.
- **Secondary campaigns:** 175 effective focuses per supported campaign, including at least 38 country-specific focuses.

### France

France combines the focus tree with decision-driven campaign systems for:

- the Estates-General, revolutionary assemblies, Girondin/Jacobin politics, assignats, the Vendée, the Committee of Public Safety, the Terror and Thermidor;
- Bonaparte's Italian and Egyptian campaigns, personal prestige, Brumaire, the Consulate, the Empire, coronation and the Marshals;
- the Continental System, including enforcement pressure and foreign evasion;
- the Peninsular War, with resistance, supply pressure and bounded settlement/withdrawal outcomes;
- the Russian campaign, with preparation, depots, cohesion, attrition, retreat and non-scripted victory/defeat outcomes;
- abdication, the Bourbon Restoration, the Hundred Days and the postwar European settlement.

### Warfare and campaign systems

The mod replaces vanilla-era assumptions with Napoleonic infantry, cavalry, artillery, support units, equipment and age-of-sail naval technology.

Shared campaign mechanics include treasury, debt, legitimacy, political fervour, war exhaustion, army prestige, reform and foreign-campaign supply pressure. Coalition wars use bounded scripted settlements instead of unrestricted vanilla total-war annexation.

### Territorial and diplomatic systems

- historical/formable-only coring;
- explicit formable state and core catalogues;
- normal HOI4 puppet relationships for restored/client states;
- seven coalition rounds with consent, subsidy and separate-peace mechanics;
- Europe-centred campaign scope with relevant North African, Atlantic and Indian states represented where approved.

### Presentation

The mod includes generated period-style focus art, portraits, event pictures, flags, loading screens, UI elements and a small provenance-tracked soundtrack. English is the maintained localisation language.

## Start date and compatibility

- **Start date:** 5 May 1789
- **Campaign end:** open-ended
- **Target HOI4 version:** 1.19.x
- **Required DLC:** La Résistance

This is an active development build. Script and regression tests are extensive, but a clean in-engine campaign is still the final authority for compatibility and balance.

## Installation

1. Download or clone the repository into a Hearts of Iron IV mod directory.
2. Point a launcher .mod descriptor at the directory containing descriptor.mod.
3. Enable the mod in its own playset.
4. Start a new 1789 campaign.

For development testing, launching HOI4 with -debug and checking error.log / game.log is strongly recommended.

## Repository structure

~~~text
content/                  Source-owned content generators and registries
common/                   Focuses, decisions, ideas, units, technologies and scripted mechanics
history/                  Country setup and starting OOB data
events/                   Narrative and mechanical events
localisation/english/     Maintained English localisation
interface/ and gfx/       UI registrations and generated visual assets
music/ and sound/         Soundtrack and event audio
tests/                    Regression and structural tests
tools/                    Content compiler and validation tooling
docs/                     Design, scope and generated reference documentation
~~~

## Building from source

Most large content systems are authored under content/build_*.py and compiled into checked-in HOI4 files.

~~~sh
python3 tools/build_content.py
python3 tools/build_content.py --check
python3 -m unittest discover -s tests -v
python3 tools/check_content.py
~~~

Edit the source generator or registry that owns a generated file rather than hand-editing compiled output. Ownership is recorded in docs/generated_manifest.json.

## Project documentation

- [ROADMAP.md](ROADMAP.md) — current implementation and acceptance status.
- [suggestions.md](suggestions.md) — forward-looking proposals and priorities.
- [Detailed milestone catalogue](docs/roadmap-milestones.md) — retained milestone checklists.
- [France decision mechanics](docs/france-decision-mechanics.md) — current French decision-system design.
- [Generated manifest](docs/generated_manifest.json) — generated-file ownership and hashes.

## Development status

The project already has broad campaign content. The main remaining work is **runtime certification, bespoke historical depth outside France, AI/pacing, map/OOB accuracy and balance based on actual campaign evidence**, not raw focus-count expansion.
'''
    suggestions = '''# Suggestions

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

### France — decision mechanics implemented

The six former France proposals are now implemented in the source-owned decision layer: revolutionary crisis management, Bonaparte's prestige/rise, Continental enforcement and evasion, Peninsular resistance, Russian campaign logistics/outcomes, and the 1814–1815 restoration cycle.

Next France priorities:
- Runtime-balance the new 0–100 crisis/campaign meters so choices are consequential without becoming repetitive click maintenance.
- Add more bespoke narrative events around decision thresholds, especially the Vendée, assignat crisis, Italian/Egyptian campaign outcomes and Russian retreat.
- Replace the remaining date-driven French-adjacent European collapse events where state-driven triggers would produce better campaigns.
- Give the most important decision systems dedicated UI/tooltips only after their ordinary decision presentation is proven insufficient in game.
- Measure AI use of the decision systems and tune decision weights so historical AI can progress without being railroaded into a fixed outcome.

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
'''
    contracts = '''# Repository source contracts

The initial GitHub import omitted country tags, country definitions, ideology subtypes, leader traits and some assets present in the uploaded mod. New content must not depend on an archive outside this repository.

The builder restores the 68-tag namespace and colour palette, supplies referenced subtypes/traits and generates correctly sized original placeholder flags and bookmark artwork. These graphics are not final historical designs.

PRU, HOL and GER overlap vanilla identities. Vanilla country-tag load order, country-history overlays and the remaining world require a real installed-definition/engine audit. This pass does not conceal the risk by deleting the entire vanilla database.

Legacy focus/event/technology localisation prose is still a separate reconciliation item. Missing translations are content defects; they do not themselves prove a startup crash. Original architecture documentation is retained, not treated as runtime evidence.
'''
    return {'README.md':readme, 'ROADMAP.md':roadmap, 'suggestions.md':suggestions, 'docs/source-contracts.md':contracts}
