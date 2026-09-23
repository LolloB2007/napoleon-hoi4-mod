# Napoleonic Era

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
