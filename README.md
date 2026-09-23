# Napoleonic Era for Hearts of Iron IV

A Europe-first campaign beginning on **5 May 1789**, centred on the French Revolution and the Napoleonic Wars. France is the narrative centre; Britain, Habsburg Austria, Prussia and Russia are the other great-power campaigns.

**Current branch: A01-A12 implemented in the stacked approval series; static validation and HOI4 runtime certification remain**

> Development build, not a verified release. Static tests do not demonstrate a successful HOI4 launch or balanced campaign.

## Project documents

- [ROADMAP.md](ROADMAP.md): live implementation and acceptance status.
- [Detailed milestone catalogue](docs/roadmap-milestones.md): all retained milestone checklists.
- [to ask lollo.md](to%20ask%20lollo.md): owner decisions awaiting approval.
- [suggestions.md](suggestions.md): proposals, not silently enabled changes.
- [Legacy architecture](docs/legacy-architecture.md): retained earlier documentation; historic counts and completion claims are superseded by the current roadmap.

## Campaign and political paths

The inherited framework starts in 1789. Under approved A01, historical dates are minimum focus gates rather than autonomous event timers; A02 removes the practical campaign end. Development follows playable slices: 1789-1795, 1796-1804, 1805-1807, 1808-1811 and 1812-1815.

France retains constitutional-monarchy, revolutionary-republican, royalist and Bonapartist routes. The end-product requirement is at least **450 distinct French focuses**, different durations, meaningful policy choices, many events, territorial integration and client-state interactions. A node-count target alone is not campaign completion.

The engine slots map neutrality to Absolutism, democratic to Constitutionalism, communism to Republicanism and fascism to Bonapartism. These are technical identifiers, not historical equivalences between eighteenth- and twentieth-century movements.

## Existing foundations and this branch

The project includes five major trees, sixteen secondary-country setups, national spirits, technologies, custom infantry/cavalry/artillery/support units, equipment and standing OOBs. Missing source contracts are restored in this branch. Flags and bookmark artwork are placeholders, not researched final art. Country-history overlays and the untouched vanilla world still require an engine/database audit.

The four opening northern and Ottoman conflicts use bounded scripted peace. The purpose is to avoid full annexations through vanilla total-war peace conferences. Alternate-winner terms require approval; current hooks need real engine testing, especially simultaneous wars and third-party intervention.

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

A01-A12 add regression coverage for chronology gates, open-ended campaign, outcome-aware settlements, coring/formables/clients, geographic scope, DLC baseline, alternate-route plausibility, presentation, music provenance, and English-only localisation. GitHub Actions and a real HOI4 1.19.x + La Résistance launch remain the final certification gates.

The structural parser understands comments, quoted strings, lists and nested blocks; graph tests detect missing prerequisites and cycles. It is not the Paradox engine. Braces and references do not establish modifier validity, correct scope, OOB deployment timing or peace-conference interception.

New mechanics need explicit scope, costs, repeatability and cleanup. Territorial transfers must verify ownership and protect third-party land. Peace effects need idempotency and recursion guards. Events must recheck routes when effects execute, not merely when queued. Do not restore version-specific state files without checking the installed map.

## Contribution and acceptance

Use a branch per milestone or named general pass. Include merge dependencies, exact delivered scope, evidence, runtime limits and approval blockers. Update the three tracking documents through content/status.json and the documentation builder. Milestone 7 requires campaign measurements; Milestone 9 requires rights-cleared assets and an in-game presentation review.
