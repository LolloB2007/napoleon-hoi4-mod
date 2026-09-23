"""Generate the owner's three tracking documents from branch status."""
import json

QUESTIONS = [
('A01','Calendar model','Historical chronology policy.','APPROVED: historical dates are minimum-date focus gates only; events, wars and peace deals are state-driven.'),
('A02','Campaign end','Campaign end policy.','APPROVED: remove the practical campaign end and allow open-ended continuation.'),
('A03','Alternate peace outcomes','Bounded-war settlement policy.','APPROVED: settlements follow the actual victor and war objectives; no unrestricted annexation.'),
('A04','Coring policy','Coring and occupation policy.','APPROVED: no broad conquest coring; only historical/formable cores, with targeted compliance support where appropriate.'),
('A05','Formable catalogue','Formable policy.','APPROVED IN PRINCIPLE: conventional and limited credible alternate formables with explicit founders and borders.'),
('A06','Clients and releasables','Client-state policy.','APPROVED: standard HOI4 puppet relationships are the default; never transfer unrelated third-party land.'),
('A07','Geographic scope','World-scope policy.','APPROVED: Europe plus relevant colonial possessions, North Africa, USA, Canada and India; irrelevant regions may remain inert/abstract.'),
('A08','Compatibility baseline','Compatibility policy.','APPROVED: target HOI4 1.19.x and require La Résistance; runtime compatibility still needs a real launch.'),
('A09','Alternate-route limits','Alternate-history policy.','APPROVED: credible historical near-counterfactuals and plausible dynastic/political alternatives; no meme/fantasy routes.'),
('A10','Visual and map art direction','Presentation policy.','APPROVED: painted/historical scenes and portraits, engraved/cartographic UI and focus art, understated period map styling.'),
('A11','Soundtrack direction','Music policy.','APPROVED: original scoring plus newly rendered public-domain Revolutionary/Napoleonic repertoire, with provenance.'),
('A12','Translation scope','Localisation policy.','APPROVED: English only for now; community translations may be accepted later, but no machine-translated release padding.')]


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

## Approval and development rules

The queue is [to ask lollo.md](to%20ask%20lollo.md). **Revisit scripted peace deals when the historically losing side wins.** A01-A12 are approved implementation policy. New decisions that materially change them require a new owner entry.

Each milestone gets its own PR, even when only an explicitly identified slice is implemented. Dependent PRs may be stacked: merge the parent first, then retarget its child to master. No workflow merges PRs. Every PR keeps README, this roadmap, the approval queue and test evidence current.

Build playable historical slices: **1789-1795 > 1796-1804 > 1805-1807 > 1808-1811 > 1812-1815**. Do not equate generated file counts with finished campaigns.
'''
    asks = f'''# To ask Lollo

{header}

This is the owner-decision register. A01-A12 are approved; implementation status is tracked separately. Existing French routes, ordinary implementation and validation are authorized. The current owner target is 600-650 French focuses, 350-400 for each other major, and 150-200 for each secondary campaign with at least 30-40 country-specific focuses. Approving a PR does not approve all proposals listed here.

'''
    for key,title,question,default in QUESTIONS:
        asks += f'## {key}: {title}\n\n**Approved.** {default}\n\n'
    asks += '## Not approval blockers\n\nNamespacing, missing references, scope corrections, finite costs, cooldowns, idempotency, localisation encoding, tests and preserving existing work can proceed. Prototype balance numbers remain provisional until campaign testing.\n'
    readme = f'''# Napoleonic Era for Hearts of Iron IV

A Europe-first campaign beginning on **5 May 1789**, centred on the French Revolution and the Napoleonic Wars. France is the narrative centre; Britain, Habsburg Austria, Prussia and Russia are the other great-power campaigns.

{header}

> Development build, not a verified release. Static tests do not demonstrate a successful HOI4 launch or balanced campaign.

## Project documents

- [ROADMAP.md](ROADMAP.md): live implementation and acceptance status.
- [Detailed milestone catalogue](docs/roadmap-milestones.md): all retained milestone checklists.
- [to ask lollo.md](to%20ask%20lollo.md): owner decisions awaiting approval.
- [suggestions.md](suggestions.md): proposals, not silently enabled changes.
- [Legacy architecture](docs/legacy-architecture.md): retained earlier documentation; historic counts and completion claims are superseded by the current roadmap.

## Campaign and political paths

The inherited framework starts in 1789. Under approved A01, historical dates are minimum focus gates rather than autonomous event timers; A02 removes the practical campaign end. Development follows playable slices: 1789-1795, 1796-1804, 1805-1807, 1808-1811 and 1812-1815.

France retains constitutional-monarchy, revolutionary-republican, royalist and Bonapartist routes. The current content target is **600-650 French focuses**, with **350-400** for each other major and **150-200** for each secondary campaign with substantial personalised material. A node-count target alone is not campaign completion.

The engine slots map neutrality to Absolutism, democratic to Constitutionalism, communism to Republicanism and fascism to Bonapartism. These are technical identifiers, not historical equivalences between eighteenth- and twentieth-century movements.

## Existing foundations and this branch

The project includes five major trees, sixteen secondary-country setups, national spirits, technologies, custom infantry/cavalry/artillery/support units, equipment and standing OOBs. Missing source contracts are restored in this branch. Flags and bookmark artwork are placeholders, not researched final art. Country-history overlays and the untouched vanilla world still require an engine/database audit.

The four opening northern and Ottoman conflicts use bounded scripted peace. The purpose is to avoid full annexations through vanilla total-war peace conferences. Alternate-winner terms require approval; current hooks need real engine testing, especially simultaneous wars and third-party intervention.

{delivered}

## Installation for testing

1. Download the **complete branch**, not just a PR patch, into a local HOI4 mod directory.
2. Create/update the launcher's external .mod file to point to the directory containing descriptor.mod. Do not hardcode another contributor's local path.
3. Enable only this mod in a separate test playset and start a **new** 1789 campaign.
4. Launch with -debug. Inspect error.log and game.log under the Hearts of Iron IV user-data logs directory.
5. Verify rulers, territory, armies, research, focus rendering, decisions and scripted wars before a long campaign.

The inherited descriptor targets 1.19.*. Confirm your actual version/DLC configuration before treating compatibility as established. The repository does not distribute game files or guarantee save compatibility across development branches.

## Sources and build

New content is authored in content/build_*.py and compiled into ordinary checked-in .txt/.yml/.gfx/.tga files. Players do not need Python. A SHA-256 manifest identifies generated outputs and their source ownership.

```sh
python3 tools/build_content.py
python3 tools/build_content.py --check
python3 -m unittest discover -s tests -v
python3 tools/check_content.py
```

Edit the source module, not a generated output. Hand-authored files stay hand-authored unless explicitly listed in docs/generated_manifest.json. The build rejects unsafe paths and duplicate outputs.

The GitHub workflow builds and tests dev/* branches, then commits generated outputs to that same branch only. Pull-request verification is read-only. No workflow merges PRs, changes master, collects player data or launches HOI4. Write permission is limited to the generator job.

## Layout

```text
content/                  Editable content modules and branch status
common/country_tags/      Country namespace
common/countries/         Country colours and graphical cultures
common/national_focus/    Focus trees and shared branches
common/ideas/             National spirits
common/scripted_effects/  State-changing mechanics
common/scripted_triggers/ Reusable conditions
common/decisions/         Player and AI actions
common/on_actions/       Startup and periodic hooks
common/technologies/     Technologies and inherited doctrines
common/units/            Subunits and equipment
history/                 Starting governments and OOBs
events/                  Narrative and mechanical events
localisation/english/    English text with UTF-8 BOM
interface/ and gfx/      UI registrations and assets
tests/ and tools/        Build, parser and validation
docs/                   Scope, manifests and test evidence
```

## Testing limits

{report}

The structural parser understands comments, quoted strings, lists and nested blocks; graph tests detect missing prerequisites and cycles. It is not the Paradox engine. Braces and references do not establish modifier validity, correct scope, OOB deployment timing or peace-conference interception.

New mechanics need explicit scope, costs, repeatability and cleanup. Territorial transfers must verify ownership and protect third-party land. Peace effects need idempotency and recursion guards. Events must recheck routes when effects execute, not merely when queued. Do not restore version-specific state files without checking the installed map.

## Contribution and acceptance

Use a branch per milestone or named general pass. Include merge dependencies, exact delivered scope, evidence, runtime limits and approval blockers. Update the three tracking documents through content/status.json and the documentation builder. Milestone 7 requires campaign measurements; Milestone 9 requires rights-cleared assets and an in-game presentation review.
'''
    suggestions = '''# Suggestions

These are proposals, not approvals. Evaluate them against a playable campaign and record owner choices in to ask lollo.md.

| Proposal | Benefit | Trade-off / approval |
|---|---|---|
| Optional open-ended campaign | Continue beyond 1815/1821 | Needs postwar AI, research and events; A02 |
| Historical order rather than mandatory dates | Progress responds to player actions | Needs successor conditions and anti-skip guards; A01 |
| Separate historical and flexible game rules | Supports both play styles | Multiplies testing combinations; A01 |
| Outcome-aware bounded treaties | The historically losing side can gain a meaningful victory | Agree bounded terms, not unrestricted annexations; A03 |
| Route-specific integration | Coring becomes an investment rather than a conquest reward | Approve states, delay, compliance and failures; A04 |
| Formable/releasable registry | Auditable founders, borders and client status | A05/A06 |
| Temporary coalitions | Separate peace, exit and later re-entry | Prevent automatic total-war escalation and recursive calls |
| Focus panels and navigation | Keep 4,000+ campaign focus nodes usable | Requires in-game layout and accessibility testing |
| Campaign measurement fixtures | Balance organisation, supply and casualties using evidence | Manual logs/saves first; no remote player telemetry |
| Installed-definition compatibility audit | Catch unsupported effects/modifiers | Requires the user's game baseline; A08 |
| Asset provenance ledger | Avoid unlicensed redistribution | A10 |

A01-A12 remain approved policy. The current focus-depth targets and explicit formable core-state rule are owner-directed implementation work; further speculative territorial expansion still requires explicit source entries.
'''
    contracts = '''# Repository source contracts

The initial GitHub import omitted country tags, country definitions, ideology subtypes, leader traits and some assets present in the uploaded mod. New content must not depend on an archive outside this repository.

The builder restores the 68-tag namespace and colour palette, supplies referenced subtypes/traits and generates correctly sized original placeholder flags and bookmark artwork. These graphics are not final historical designs.

PRU, HOL and GER overlap vanilla identities. Vanilla country-tag load order, country-history overlays and the remaining world require a real installed-definition/engine audit. This pass does not conceal the risk by deleting the entire vanilla database.

Legacy focus/event/technology localisation prose is still a separate reconciliation item. Missing translations are content defects; they do not themselves prove a startup crash. Original architecture documentation is retained, not treated as runtime evidence.
'''
    return {'README.md':readme, 'ROADMAP.md':roadmap, 'to ask lollo.md':asks, 'suggestions.md':suggestions, 'docs/source-contracts.md':contracts}
