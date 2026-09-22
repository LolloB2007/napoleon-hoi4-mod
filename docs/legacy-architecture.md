# Napoleonic Era for Hearts of Iron IV

**Napoleonic Era** is an in-development Hearts of Iron IV total-conversion mod that moves the campaign from the Second World War to the age of the French Revolution and the Napoleonic Wars.

The campaign begins on **5 May 1789**, with the Estates-General convening at Versailles, and is designed around the political and military transformation of Europe through the Revolution, the Coalition Wars, the rise and fall of Napoleon, and the post-war settlement. The current campaign end date is **1 January 1821**.

> **Development status:** early playable framework / active migration to HOI4 1.19.x. The project has a substantial amount of content, but it is not yet a finished or balanced total conversion. Static validation is part of the repository; clean in-game launch testing remains required after engine-facing changes.

## Current target

- **Hearts of Iron IV:** 1.19.x
- **Campaign:** 5 May 1789 to 1 January 1821
- **Language:** English
- **Primary scenario:** Europe in 1789
- **Default country:** France

## What the mod currently contains

### A 1789 campaign framework

The mod replaces the normal 1936/1939 scenario flow with a single Napoleonic bookmark beginning on 5 May 1789. The engine start and end dates are overridden to match the campaign.

The 1789 political map is applied through a startup scripted effect rather than hundreds of duplicated `history/states` files. This is deliberate: vanilla state filenames can change between HOI4 versions, and overriding an old filename while the renamed vanilla file still loads can create duplicate state IDs and startup crashes.

**Do not reintroduce mass `history/states/*.txt` overrides without verifying the exact current vanilla paths.**

### Five developed major powers

The current major-country content centers on:

- **France**
- **Great Britain**
- **Habsburg Austria**
- **Prussia**
- **Russia**

Each has a custom 1789 country history, leaders, national spirits, technologies, a standing army OOB, and a national focus tree.

France is the narrative centerpiece and currently has four broad political routes:

1. **Constitutional monarchy** — preserve the Revolution's reforms without overthrowing the monarchy.
2. **Revolutionary republic** — radicalize the Revolution, proclaim the Republic, mobilize the nation, and fight the monarchies of Europe.
3. **Bonapartism** — emerge from the revolutionary route through Brumaire, the Consulate, and the French Empire.
4. **Bourbon counter-revolution** — suppress the Revolution and restore the Ancien Régime.

Route flags explicitly isolate these paths so the historical revolutionary timeline cannot silently hijack a constitutional or royalist France.

### Historical event spine, 1789-1815

The event system provides a historical backbone while still allowing alternate outcomes. Major scripted milestones include:

- Storming of the Bastille
- Declaration of the Rights of Man
- Flight to Varennes
- War of the First Coalition
- Proclamation of the French Republic
- Execution of Louis XVI
- Reign of Terror
- Thermidor
- The Directory
- 18 Brumaire
- Proclamation and coronation of the French Empire
- Trafalgar
- Austerlitz
- Confederation of the Rhine and dissolution of the Holy Roman Empire
- Jena-Auerstedt
- Continental System
- Tilsit
- Invasion of Russia
- Retreat from Moscow
- Prussian War of Liberation
- Leipzig
- First Bourbon Restoration
- Hundred Days
- Waterloo
- Second Abdication
- Concert of Europe

The event chain uses country and global flags as a state machine. Alternative French political routes are now gated explicitly so events only advance when their underlying political route exists.

## Political system

HOI4's four hardcoded ideology families are repurposed for the period:

| HOI4 internal ideology | Napoleonic Era interpretation |
| --- | --- |
| `neutrality` | Absolutism / traditional monarchy |
| `democratic` | Constitutionalism |
| `communism` | Republicanism / Jacobinism |
| `fascism` | Bonapartism |

The internal names still appear in script because the engine expects them. Player-facing localisation uses the period-appropriate political terminology.

## National spirits and ideas

Custom ideas are enabled for the major powers and for campaign-wide systems. They represent political institutions, military traditions, economic conditions, revolutionary mobilization, reform programs, logistics, coalition politics, and the changing regimes of France.

Examples include:

- Bourbon Crisis
- Revolutionary Republic
- Levée en Masse
- Reign of Terror
- Directory Corruption
- Empire of the French
- Continental System
- Royal Navy Supremacy
- Industrial Revolution
- Josephine reforms
- Frederician inheritance
- Scharnhorst reforms
- Russian winter and vast distances
- Concert of Europe

Focuses and events add or remove these ideas directly; active idea references are statically validated.

## Napoleonic military system

The mod contains a custom land-combat framework intended to make HOI4 divisions represent formations closer to Napoleonic corps and brigades than twentieth-century mechanized armies.

### Custom subunits

The enabled land stack includes 19 custom subunits across infantry, cavalry, artillery, and support roles, including:

- Line infantry
- Light infantry
- Grenadiers
- Militia
- Guard infantry
- Light cavalry
- Dragoons
- Heavy cavalry
- Lancers
- Irregular cavalry / Cossack-style formations
- Foot artillery
- Horse artillery
- Siege artillery
- Sappers
- Train battalions
- Field hospitals
- Staff companies
- Square-drill support
- Signal corps

Custom subunits use current vanilla-safe unit classifications such as `category_all_infantry`, `category_artillery`, and `category_support_battalions`. Cavalry is explicitly classified as cavalry. These classifications are important because HOI4's AI and combat triggers query them internally.

### Equipment

The custom equipment stack includes period-specific lines for:

- Muskets
- Cavalry equipment
- Artillery
- Support equipment
- Supply wagons
- Reconnaissance/intelligence corps equipment
- Age-of-sail naval hulls

Custom artillery and support equipment use Napoleonic namespaced database IDs rather than redefining vanilla `artillery_equipment` or `support_equipment` from a second file.

### Technologies

The current technology layer contains 83 custom technologies covering:

- Infantry and musket development
- Cavalry organization
- Artillery systems
- Support and logistics
- Reconnaissance / communications / intelligence
- Age-of-sail naval development
- Land doctrine

Custom technology categories are defined in `common/technology_tags/00_napoleonic_tags.txt` and are used by focus research bonuses.

### Land doctrines

Four mutually exclusive doctrine families are implemented:

- **Line Doctrine** — disciplined volley fire, defensive solidity, squares, and reverse-slope tactics.
- **Column Doctrine** — massed attack columns, élan, speed, and offensive concentration.
- **Skirmisher Doctrine** — dispersed light troops, mobility, terrain use, and resilience away from supply.
- **Combined Arms Doctrine** — corps organization, cavalry-artillery coordination, concentration, and operational command.

The vanilla WWII grand doctrines are hidden for the Napoleonic scenario. The current doctrine implementation uses the technology-based doctrine system; a future migration to the newer grand-doctrine framework can be considered separately without blocking content development.

## Starting armies

France, Great Britain, Austria, Prussia, and Russia load custom standing OOBs at the 1789 start.

The OOBs define custom division templates and deployed formations using the Napoleonic subunit stack. They are statically checked against the enabled subunit database so an OOB cannot reference a missing custom battalion unnoticed.

Additional event-specific OOBs currently include the French National Guard and émigré returners.

Naval starting OOBs remain separate from the land-army restoration and should be considered unverified until their ports and fleet composition have been tested in-game on the current map version.

## Repository structure

Important directories:

```text
common/
  bookmarks/             1789 scenario bookmark
  defines/               campaign start/end dates
  doctrines/             grand-doctrine overrides
  ideas/                 national spirits and campaign ideas
  national_focus/        major-power focus trees
  on_actions/            startup hooks
  scripted_effects/      reusable scripted effects, including 1789 ownership
  technologies/          Napoleonic technology and doctrine trees
  technology_tags/       custom technology categories/folders
  units/                  custom land subunits and equipment

events/                   Revolution, Napoleonic Wars, and collapse timeline
history/
  countries/              1789 major-country setup
  units/                  starting and event OOBs
localisation/english/      English localisation
tools/                     static validation utilities
docs/                      audits, reports, and development notes
```

## Installation for development

This repository is intended to contain the **contents of the mod directory**.

A typical manual installation is:

1. Clone the repository into your Hearts of Iron IV mod directory, for example:
   - Windows: `Documents/Paradox Interactive/Hearts of Iron IV/mod/napoleon-hoi4-mod`
   - macOS: `~/Documents/Paradox Interactive/Hearts of Iron IV/mod/napoleon-hoi4-mod`
   - Linux: `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/napoleon-hoi4-mod` or the equivalent Paradox user directory on your installation.
2. Create or update the launcher `.mod` file in the parent `mod` directory so its `path` points to the cloned repository.
3. Enable the mod in the Paradox launcher.
4. Run HOI4 with no unrelated gameplay mods enabled while testing migration issues.

A minimal launcher descriptor looks like:

```text
name="Napoleonic Era"
path="/absolute/path/to/napoleon-hoi4-mod"
supported_version="1.19.*"
```

The repository's own `descriptor.mod` contains the mod metadata used by the launcher/Workshop packaging flow.

## Validation and debugging

Run the static validators from the repository root:

```bash
python3 tools/check_braces.py
python3 tools/find_missing_oobs.py
python3 tools/find_invalid_state_refs.py
python3 tools/validate_references.py
python3 tools/find_missing_localisation.py
python3 tools/find_duplicate_ids.py
python3 tools/validate_military_stack.py
```

`validate_military_stack.py` additionally checks that:

- starting technologies exist;
- technology equipment and subunit unlocks resolve;
- custom technology categories resolve;
- subunit equipment requirements resolve;
- every custom battalion used by an OOB exists;
- the five major powers actually load their 1789 OOBs;
- known vanilla artillery/support equipment IDs are not accidentally redefined;
- the legacy invalid `category_x = 1` technology syntax does not return;
- restored land units retain the classifications required by engine/AI queries.

Static validation is not a substitute for launching the game. For engine-facing changes, the final check is a clean HOI4 1.19.x boot with debug logging and inspection of the Paradox logs, especially `error.log` and `game.log`.

## Development rules that matter

### Do not duplicate vanilla state IDs through mismatched filenames

The 1789 map currently transfers state ownership at startup. This avoids the historical crash class where an old mod state filename and a renamed vanilla state file both load and define the same numeric state ID.

### Avoid vanilla database-ID collisions unless intentionally replacing the exact vanilla path

Adding a second definition of a hardcoded database ID is not the same thing as safely overriding the vanilla file. Custom equipment, units, technologies, ideas, and similar database objects should normally use unique IDs.

### Keep route logic explicit

French constitutional, revolutionary, royalist, and Bonapartist progression is represented by dedicated route flags. Events that belong to one route should check that route rather than inferring it from a loosely related historical flag.

### Keep mechanical IDs stable once content depends on them

Focuses and events already reference the Napoleonic idea, technology-category, subunit, and equipment interfaces. Balance values can be changed later without forcing content rewrites; renaming public IDs should be treated as a migration.

### Validate before adding another layer

HOI4 often tolerates one malformed or unresolved object long enough to make the eventual failure look unrelated. Run the validators after changes to focuses, events, ideas, OOBs, technologies, or unit definitions.

## Known limitations / work still ahead

The project is deliberately not claiming to be finished. Current known areas for future work include:

- real in-game 1.19.x launch validation after each restoration/migration pass;
- balance of the restored land combat and doctrine systems;
- broader country histories and content for secondary European powers;
- verified starting naval OOBs and deeper age-of-sail naval balance;
- decisions and missions that were previously disabled during crash isolation;
- portraits, focus icons, event art, and other presentation work;
- additional diplomacy and coalition logic;
- economy/industry conversion away from twentieth-century assumptions;
- AI tuning for the 1789-1815 military system;
- eventual consideration of the modern grand-doctrine framework;
- later-world and post-1815 content where appropriate.

## Historical design philosophy

The mod is intended to be **historically grounded rather than historically deterministic**. The French Revolution and Napoleonic Wars provide a strong scripted historical spine, but the player should be able to create coherent alternatives without the historical event chain forcing the original outcome back onto the campaign.

The same principle applies to military systems: the goal is not to force HOI4 to become a perfect tactical simulation of 1805. It is to use the engine's strategic systems to make manpower, organization, cavalry, artillery, doctrine, logistics, leadership, coalitions, and political legitimacy matter in ways that feel recognizably Napoleonic.

## Contributing

The project is currently under active development. Before opening a content PR:

1. keep script IDs stable and namespaced where practical;
2. avoid adding new vanilla-path overrides unless the override is intentional and checked against the current game version;
3. run the validation suite;
4. describe any new route flags, scripted effects, or cross-file dependencies in the PR;
5. call out anything that still requires an in-game test.

If a change touches map files, equipment databases, unit classifications, doctrine systems, or the campaign bookmark, treat it as engine-facing and test it separately from large batches of narrative content.

---

**Current priority:** establish a stable 1789 foundation on HOI4 1.19.x, then return to expanding country content, events, diplomacy, and the wider Napoleonic world.
