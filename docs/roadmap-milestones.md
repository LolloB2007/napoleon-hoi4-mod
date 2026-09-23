# Napoleonic Era — Development Roadmap

This document tracks the major development work required after the core startup/stabilisation pass.

> **Scope:** This roadmap intentionally begins after the launch/debug and immediate runtime-cleanup steps. Those are operational prerequisites rather than long-term content milestones.
>
> **Status convention:** Check items off as they are completed. A milestone should only be considered complete when its **Done when** criteria are satisfied.

---

## Milestone 1 — Finish the 1789 Starting World

Build the secondary powers into proper 1789 countries rather than allowing vanilla-era setup to leak into the campaign.

### Priority countries

- [x] Spain
- [x] Portugal
- [x] Ottoman Empire
- [x] Sweden
- [x] Denmark–Norway
- [x] Polish–Lithuanian Commonwealth
- [x] Netherlands
- [x] Kingdom of Naples
- [x] Sardinia–Piedmont
- [x] Venice
- [x] Papal States
- [x] Tuscany
- [x] Bavaria
- [x] Saxony
- [x] Hanover
- [x] Württemberg

### For each country

- [x] Correct 1789 government and ideology
- [x] Correct ruler / political leadership
- [x] Appropriate starting national spirits
- [x] Correct diplomatic relationships
- [x] Appropriate starting technologies
- [x] Historically plausible starting army where relevant
- [x] Correct ownership / cores / claims where needed
- [x] Remove obvious vanilla 1936 carry-over

### Done when

A 1789 start produces a broadly credible European political map and the major secondary states no longer behave like renamed 1936 countries.

> **Implementation note:** Baseline diplomatic opinions are included here. Runtime smoke-testing remains required before declaring the wider campaign slice complete.

---

## Milestone 2 — Make 1789 Diplomacy Real

Turn historical relationships and ongoing conflicts into actual game state rather than narrative flags.

### Active wars

- [x] Russo–Turkish War
- [x] Russo–Swedish War
- [x] Austrian involvement against the Ottoman Empire where appropriate

### Diplomatic structure

- [x] British–Hanoverian relationship
- [x] Austrian Habsburg possessions and dependencies
- [x] Polish geopolitical situation
- [x] Relevant guarantees
- [x] Relevant alliances
- [x] Relevant subjects / personal-union-style relationships
- [x] Holy Roman Empire relationships where useful to gameplay
- [x] Initial rivalries and strategic hostility

### Done when

The diplomatic screen on 5 May 1789 tells roughly the same geopolitical story as the historical situation, and the wars already underway are mechanically real.

> **Implementation note:** The opening wars are deliberately bounded scripted conflicts rather than normal HOI4 total wars. The Theatre War ends by July 1789, the Russo–Swedish War by the Treaty of Värälä, the Austro–Turkish War by Sistova, and the Russo–Turkish War by Jassy. An `on_capitulation_immediate` guard applies the same limited settlements early if a belligerent collapses, preventing ahistorical full annexations. Jassy transfers only the Odessa/Yedisan state abstraction to Russia. Runtime smoke-testing remains pending.
>
> **Future revisit:** The scripted peace system currently prioritises historical / bounded settlements. It must be revisited once non-historical paths are developed so that a decisive victory by the historically losing side can produce an appropriate alternate settlement instead of being forced back into the historical treaty outcome.

---

## Milestone 3 — Make France Content-Complete

France is the central campaign and should become the first fully developed nation.

### Revolution and constitutional crisis

- [ ] Estates-General mechanics
- [ ] National Assembly
- [ ] Legislative Assembly
- [ ] National Convention
- [ ] Constitutional-monarchy route depth
- [ ] Royalist counter-revolution route depth
- [ ] Republican route depth
- [ ] Jacobins vs Girondins
- [ ] Political radicalisation mechanics
- [ ] Vendée / internal counter-revolution
- [ ] Assignats and revolutionary financial crisis
- [ ] Committee of Public Safety
- [ ] Reign of Terror consequences
- [ ] Thermidorian Reaction
- [ ] Directory instability

### Napoleon's rise

- [ ] Italian Campaign content
- [ ] Egyptian Expedition content
- [ ] Napoleon prestige / popularity progression
- [ ] 18 Brumaire mechanics
- [ ] Consulate government
- [ ] Coronation / formation of the Empire
- [ ] Marshals of the Empire
- [ ] Imperial administration

### Imperial France

- [ ] Client-state creation
- [ ] Sister republics
- [ ] Confederation of the Rhine
- [ ] Continental System
- [ ] Continental System enforcement
- [ ] Peninsular War mechanics
- [ ] Spanish resistance / guerrilla pressure
- [ ] Russian campaign preparation
- [ ] Russian campaign logistics
- [ ] Collapse of the Grande Armée
- [ ] 1814 abdication
- [ ] Bourbon Restoration
- [ ] Hundred Days
- [ ] Final defeat / post-Napoleonic outcome

### Characters

- [ ] Expand revolutionary political characters
- [ ] Expand French generals
- [ ] Add major marshals
- [ ] Tie important characters into events, decisions and command roles

### Done when

France can be played from 1789 through 1815 on the historical route and its major alternate routes without relying on skeletal placeholder focuses or timeline events.

---

## Milestone 4 — Coalition Wars System

Replace one-off scripted coalition behavior with reusable mechanics.

### Coalition formation

- [ ] Coalition eligibility rules
- [ ] Threat / expansion checks
- [ ] Ideological reaction to revolutionary France
- [ ] Reaction to French territorial expansion
- [ ] Reaction to French client states
- [ ] Great-power coalition invitations
- [ ] AI logic for joining and leaving coalitions

### Coalition warfare

- [ ] British subsidies
- [ ] Coalition war exhaustion
- [ ] Separate-peace logic
- [ ] Peace after decisive French victories
- [ ] Defeated monarchies leaving coalitions
- [ ] Re-entry into later coalitions
- [ ] French satellite-state creation
- [ ] Sister-republic creation
- [ ] Balance-of-power reactions

### Historical coalition sequence

- [ ] First Coalition
- [ ] Second Coalition
- [ ] Third Coalition
- [ ] Fourth Coalition
- [ ] Fifth Coalition
- [ ] Sixth Coalition
- [ ] Seventh Coalition

### Done when

The First through Seventh Coalitions are generated by one coherent diplomatic framework rather than seven unrelated piles of scripted war declarations.

---

## Milestone 5 — Complete the Other Four Great Powers

Develop Britain, Austria, Prussia and Russia into full campaigns.

Recommended order:

1. Britain
2. Austria
3. Prussia
4. Russia

### Britain

- [ ] Parliamentary politics
- [ ] Royal Navy strategy
- [ ] Coalition financing
- [ ] Continental blockade
- [ ] Peninsular intervention
- [ ] Colonial / imperial commitments
- [ ] Industrial Revolution
- [ ] Historical and alternate routes

### Austria

- [ ] Joseph II reform legacy
- [ ] Conservative reaction
- [ ] Belgian unrest
- [ ] Archduke Charles military reform
- [ ] Coalition leadership
- [ ] Holy Roman Empire crisis
- [ ] Austrian Empire formation
- [ ] Metternich / postwar settlement
- [ ] Historical and alternate routes

### Prussia

- [ ] Frederician military legacy
- [ ] Pre-Jena conservatism
- [ ] Jena catastrophe
- [ ] Stein reforms
- [ ] Scharnhorst reforms
- [ ] Universal conscription
- [ ] War of Liberation
- [ ] German leadership question
- [ ] Historical and alternate routes

### Russia

- [ ] Catherine II late reign
- [ ] Russo–Turkish conflict
- [ ] Polish partitions
- [ ] Paul I
- [ ] Alexander I
- [ ] Speransky reform
- [ ] Coalition involvement
- [ ] 1812 invasion mechanics
- [ ] Scorched earth / strategic withdrawal
- [ ] March on Paris
- [ ] Holy Alliance
- [ ] Historical and alternate routes

### Done when

All five central great powers have deep campaigns with historical and credible alternate paths, and each interacts meaningfully with the coalition framework.

---

## Milestone 6 — Reusable Napoleonic Gameplay Mechanics

Create systems that make the mod play like the Napoleonic era rather than merely look like it.

### Candidate systems

- [ ] Army morale
- [ ] General prestige
- [ ] War exhaustion
- [ ] Conscription systems
- [ ] Levée en masse
- [ ] Coalition diplomacy
- [ ] Client-state management
- [ ] Continental blockade
- [ ] Revolutionary fervor
- [ ] Monarchical legitimacy
- [ ] Nationalism
- [ ] Occupation resistance
- [ ] Army reform
- [ ] Long-range campaign logistics
- [ ] Supply collapse in hostile territory
- [ ] Political consequences of military defeat

### Implementation preference

Prefer reusable:

- decisions
- variables
- scripted effects
- scripted triggers
- national spirits
- modifiers
- event targets

Avoid invasive engine-level complexity unless a mechanic cannot reasonably be represented through normal HOI4 scripting.

### Done when

Core strategic decisions of the era — mobilisation, coalition politics, legitimacy, occupation and logistics — matter mechanically in every major campaign.

---

## Milestone 7 — Balance the Military System

Balance only after representative campaigns exist.

### Infantry

- [ ] Line infantry
- [ ] Light infantry
- [ ] Grenadiers
- [ ] Guards
- [ ] Militia

### Cavalry

- [ ] Hussars / light cavalry
- [ ] Dragoons
- [ ] Cuirassiers / heavy cavalry
- [ ] Lancers
- [ ] Cossacks
- [ ] Cavalry pursuit behavior
- [ ] Cavalry shock role

### Artillery and support

- [ ] Foot artillery
- [ ] Horse artillery
- [ ] Siege artillery
- [ ] Sappers
- [ ] Wagon trains
- [ ] Medical support
- [ ] Staff / headquarters support

### Combat model

- [ ] Organisation values
- [ ] Morale / recovery
- [ ] Soft attack
- [ ] Breakthrough
- [ ] Defence
- [ ] Reinforcement
- [ ] Movement speed
- [ ] Attrition
- [ ] Supply consumption
- [ ] Manpower requirements
- [ ] Equipment costs
- [ ] Combat width
- [ ] Corps-scale division design

### Doctrine balance

- [ ] Line Doctrine
- [ ] Column Doctrine
- [ ] Skirmisher Doctrine
- [ ] Combined Arms Doctrine

### Campaign tests

- [ ] Revolutionary Wars
- [ ] 1805 campaign
- [ ] 1806 Prussian campaign
- [ ] Peninsular War
- [ ] 1812 Russian campaign
- [ ] 1813–1814 campaigns
- [ ] Waterloo

### Design objective

Winning battles should usually destroy organisation and cohesion faster than entire armies. Catastrophic campaigns should emerge primarily through defeat, pursuit, attrition, supply failure and cumulative losses rather than every battle functioning as an annihilation event.

### Done when

Different army compositions and doctrines produce recognisably different Napoleonic battlefield behavior and historical-style campaigns are possible without scripting their outcomes.

---

## Milestone 8 — Broaden Content Geographically

After the five-power core is mature, expand the playable world.

Recommended order:

- [x] Spain
- [x] Poland / Duchy of Warsaw
- [x] Ottoman Empire
- [x] Sweden
- [x] Italian states
- [x] German minors
- [x] Portugal
- [x] Netherlands
- [x] United States

### For each expansion country

- [x] Focus tree
- [x] Events
- [x] Decisions
- [x] Leaders / characters
- [x] National spirits
- [x] Military setup
- [x] Historical route
- [x] Credible alternate-history route
- [x] Interaction with major-power systems
- [x] Localisation

### Done when

Secondary powers offer distinct campaigns and participate naturally in the European systems rather than existing only as targets for the five great powers.

**Implementation status:** complete. Thirteen campaign packs provide 299 focuses, 52 events, 39 recurring decisions and 65 national spirits. Existing European 1789 histories/OOBs remain the military baseline; the shared German campaign also fills missing political histories for Baden, Hesse and Mecklenburg, while the United States receives a Washington-era political/character baseline. WAR, BAT and HOL inherit the relevant Polish or Dutch campaign when they exist. Territorial integration, formable borders and a detailed North American map remain approval-gated rather than being silently inferred. Runtime acceptance in HOI4 is still pending.

---

## Milestone 9 — Polish and Presentation

Do expensive presentation work after the underlying campaigns are stable.

### Visuals

- [x] Unique leader portraits — original procedural portrait cards wired to current leaders
- [x] Unique marshal / general portraits — original procedural portrait cards wired to current commanders
- [x] Unique focus icons — deterministic original icon per current focus ID
- [x] Regime-specific flags — generated default + four political-slot variants
- [x] Event pictures — custom period-styled event art replaces vanilla-WWII event imagery
- [x] Loading screens — three original Napoleonic loading screens
- [x] Bookmark artwork — original 1789 bookmark art
- [ ] Custom map aesthetics — final terrain/map treatment requires A10
- [x] UI improvements where useful — common seals, dividers and presentation sprites

### Audio

- [ ] Period-appropriate music — final soundtrack direction requires A11
- [ ] Music categories / station — implement with the approved A11 soundtrack
- [x] Event audio where appropriate — original generated dispatch, crowd and artillery stingers

### Historical flavour

- [x] Historical unit names
- [x] Historical army / corps names — the mod's corps-scale division naming groups now use period formations/patterns
- [x] Historical ship names
- [x] Expanded flavour events
- [x] Expanded descriptions and tooltips

### Localisation

- [x] Final English localisation pass — first full mechanical/prose cleanup complete
- [x] Terminology consistency
- [x] Remove placeholder text from player-facing localisation
- [ ] Additional languages if contributors are available — scope/maintenance requires A12

### Done when

The non-gated implementation is complete. Final Milestone 9 acceptance still requires owner decisions on A10 (visual/map direction), A11 (soundtrack strategy) and A12 (translation scope), followed by an in-game presentation review. The current assets are original and redistribution-safe; they are deliberately replaceable if the approved art direction changes.

---

# Development Sequence

The preferred development method is chronological. Each era should become genuinely playable before moving deeply into the next.

## Phase A — 1789–1795

- [x] Complete the 1789 starting world
- [x] Real starting diplomacy and wars
- [ ] Full early French Revolution
- [ ] Constitutional / Republican / Royalist route separation
- [ ] First Coalition
- [ ] Terror and Thermidor
- [ ] Directory
- [ ] Functional warfare and technology progression

### Playable milestone: **1789–1795**

This is the first major target.

The milestone is achieved when:

- [ ] Europe looks broadly correct on 5 May 1789
- [ ] Starting armies exist and function
- [x] Existing wars are real
- [ ] France can pursue Constitutional, Republican or Royalist routes without route contamination
- [ ] Revolutionary Wars occur coherently
- [ ] Britain, Austria, Prussia and Russia react plausibly
- [ ] Technology, equipment and doctrines function
- [ ] No major recurring error-log spam is present

Once this milestone is reached, infrastructure work should stop unless a later feature genuinely requires it.

---

## Phase B — 1796–1804

- [ ] Italian Campaign
- [ ] Egyptian Expedition
- [ ] Second Coalition
- [ ] Directory instability
- [ ] 18 Brumaire
- [ ] Consulate
- [ ] Napoleonic domestic consolidation
- [ ] Coronation and creation of the Empire

---

## Phase C — 1805–1807

- [ ] Third Coalition
- [ ] Trafalgar
- [ ] Ulm / Austerlitz campaign
- [ ] Treaty of Pressburg
- [ ] End of the Holy Roman Empire
- [ ] Confederation of the Rhine
- [ ] Fourth Coalition
- [ ] Jena–Auerstedt
- [ ] Tilsit
- [ ] Continental System

---

## Phase D — 1808–1811

- [ ] Peninsular War
- [ ] Spanish resistance
- [ ] British intervention in Iberia
- [ ] Fifth Coalition
- [ ] Austrian reform and renewed war
- [ ] French imperial administration
- [ ] Continental System pressure

---

## Phase E — 1812–1815

- [ ] Invasion of Russia
- [ ] Russian strategic withdrawal
- [ ] Moscow
- [ ] Grande Armée collapse
- [ ] Prussian War of Liberation
- [ ] Sixth Coalition
- [ ] Leipzig
- [ ] Invasion of France
- [ ] First abdication
- [ ] Bourbon Restoration
- [ ] Hundred Days
- [ ] Seventh Coalition
- [ ] Waterloo
- [ ] Second abdication
- [ ] Concert of Europe

---

# Project Status Summary

| Area | Status |
|---|---|
| Startup / parser stabilisation | Foundation completed; runtime testing remains ongoing |
| Ideas / national spirits | Restored |
| Technologies | Restored |
| Custom units | Restored |
| Doctrines | Restored |
| Major-power standing OOBs | Restored |
| French route hardening | Initial pass completed |
| 1789 secondary-power setup | Implemented; runtime validation pending |
| 1789 diplomatic setup | Implemented with bounded treaty system; runtime validation pending |
| France deep-content pass | Not started |
| Coalition system | Not started |
| Britain deep-content pass | Not started |
| Austria deep-content pass | Not started |
| Prussia deep-content pass | Not started |
| Russia deep-content pass | Not started |
| Reusable era mechanics | Not started |
| Military balance pass | Not started |
| Geographic expansion | Not started |
| Final polish | Not started |

---

## Guiding Principle

Build **playable historical slices**, not hundreds of disconnected unfinished features.

The roadmap therefore advances chronologically:

**1789–1795 → 1796–1804 → 1805–1807 → 1808–1811 → 1812–1815**

Each completed period should be capable of standing on its own as a coherent campaign before the project moves substantially further forward.
