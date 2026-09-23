# To ask Lollo

**Current status: A01–A12 owner decisions recorded; next pass is implementation of the approved decisions**

This is the live approval queue. No answer is presumed. Existing French routes, ordinary implementation, validation and the target of at least 450 focuses are authorized. Approving a PR does not approve all proposals listed here.

## A01: Calendar model

**Awaiting approval.** Keep mandatory historical dates, use historical order, or offer both as game rules?

Safe interim policy: Keep inherited date gates until approved.

## A02: Campaign end

**Awaiting approval.** Remove or extend the 1821 end-date define, and what postwar progression should follow?

Safe interim policy: Keep the inherited end date.

## A03: Alternate peace outcomes

**Awaiting approval.** Approve bounded territorial and political terms when the historically losing side wins.

Safe interim policy: Preserve limited settlements; no unrestricted annexation.

## A04: Coring policy

**Awaiting approval.** Approve the eligible states, route restrictions, peace/compliance requirements and integration delay.

Safe interim policy: Preserve existing cores; do not grant broad conquest cores.

## A05: Formable catalogue

**Awaiting approval.** Approve founders and borders for Italy, Germany, Scandinavia, a restored Commonwealth and imperial federations.

Safe interim policy: Prepare an auditable registry; speculative unions remain disabled.

## A06: Clients and releasables

**Awaiting approval.** Which clients should be puppets, independent allies, personal unions or occupation governments?

Safe interim policy: Never transfer unrelated third-party land or silently annex existing clients.

## A07: Geographic scope

**Awaiting approval.** Keep Europe-first development or expand colonies and overseas theatres now?

Safe interim policy: Preserve existing overseas content and the current Wilderness abstraction.

## A08: Compatibility baseline

**Awaiting approval.** Confirm the installed HOI4 version and DLC set with a real launch.

Safe interim policy: Retain the inherited 1.19.* descriptor, without asserting engine compatibility.

## A09: Alternate-route limits

**Awaiting approval.** Approve speculative dynastic candidates and routes beyond the four existing French alternatives.

Safe interim policy: Constitutional, Republican, Royalist and Bonapartist routes are authorized.

## A10: Visual and map art direction

**Awaiting approval.** Choose the final presentation language for portraits, focus/event art, flags and map treatment.

Safe interim policy: Use original procedural engravings/cards and avoid invasive map recolouring.

## A11: Soundtrack direction

**Awaiting approval.** Choose the music strategy and redistribution policy for the final soundtrack.

Safe interim policy: Ship event stingers only; do not bundle third-party recordings.

## A12: Translation scope

**Awaiting approval.** Choose which languages should follow the final English pass and who maintains them.

Safe interim policy: Keep English authoritative until a maintained translation scope is approved.

## Not approval blockers

Namespacing, missing references, scope corrections, finite costs, cooldowns, idempotency, localisation encoding, tests and preserving existing work can proceed. Prototype balance numbers remain provisional until campaign testing.

## Territorial registry: actual pending entries

No entries below are authorized by this implementation PR. Update content/territorial_registry.json only after the owner decides.

| ID | Proposal | State IDs | Status |
|---|---|---|---|
| savoy | Savoy | [735] | Awaiting approval (A04) |
| austrian_netherlands | Austrian Netherlands (draft map abstraction) | [6] | Awaiting approval (A04) |
| italian_kingdom | Kingdom of Italy | Not specified | Awaiting approval (A05) |
| german_confederation | German Confederation | Not specified | Awaiting approval (A05) |
| scandinavian_union | Scandinavian Union | Not specified | Awaiting approval (A05) |
| restored_commonwealth | Restored Commonwealth | Not specified | Awaiting approval (A05) |
| danubian_federation | Danubian Federation | Not specified | Awaiting approval (A05/A09) |
| rhine_federation | Rhine Federation | Not specified | Awaiting approval (A05/A06) |


# Owner decisions recorded — 23 September 2026

These decisions supersede the interim policies above. They are implementation authority for the next development pass. Where a decision establishes a principle but still requires a concrete catalogue (for example exact formable borders), implementation should follow the approved principle and keep the concrete catalogue auditable in source.

## A01 — Calendar model: APPROVED

**Decision:** Keep historical dates as **minimum-date requirements on focuses only**.

- A focus may require that the historical date has been reached before it becomes available.
- The date is a `not_before` gate, not a forced completion date.
- Events, wars, peace deals and other systems should not be hard-forced to occur on an exact historical date merely because history did.
- Historical chronological order may still be enforced through prerequisites and state.
- Alternate-history branches may diverge after satisfying the relevant focus/date prerequisites.

## A02 — Campaign end: APPROVED

**Decision:** Remove the hard practical campaign end date.

- The campaign should be able to continue indefinitely rather than stopping at 1821.
- Post-Napoleonic progression may be added later where useful.
- No mandatory end-date game rule is required by this approval.

## A03 — Alternate peace outcomes: APPROVED

**Decision:** Use **scripted peace deals appropriate to the type and outcome of the war**.

- Do not use unrestricted vanilla peace conferences for the bounded historical wars covered by this system.
- The historical scripted treaty applies only when the historical victor/outcome is achieved.
- If the historically losing side wins, it must receive a suitable alternate scripted settlement instead of being forced into the historical deal.
- Outcomes should remain bounded by the character and objectives of the war rather than permitting arbitrary total annexation.

## A04 — Coring policy: APPROVED

**Decision:** No broad conquest coring.

- New cores should be limited to historically justified territory and approved formable-nation territory.
- Ordinary conquest should not eventually become core territory merely through time/compliance.
- Selected focuses and scripted peace deals may grant **compliance boosts** in territories where a country has a defined historical/strategic interest.
- Compliance bonuses do not themselves create cores.

## A05 — Formable catalogue: APPROVED IN PRINCIPLE

**Decision:** Use the conventional formables plus a limited number of credible alternate-history formables.

Approved direction includes:
- Italy
- Germany
- Scandinavia
- restored Polish-Lithuanian Commonwealth
- Rhine/German federation concepts where historically plausible
- Danubian/federal concepts where historically plausible
- a small number of additional alternate-history unions where the route has a credible political basis

Exact founders, state requirements and borders should remain explicit and auditable rather than inferred automatically.

## A06 — Clients and releasables: APPROVED

**Decision:** Use standard HOI4 **puppet relationships** as the default client-state model.

- Releasables/clients should normally become puppets.
- Do not silently transfer unrelated third-party territory.
- Special historical arrangements can still be represented through events/ideas where needed, but the mechanical subject relationship should default to puppet status.

## A07 — Geographic scope: APPROVED

**Decision:** Expand beyond Europe, but only where relevant to the European imperial system.

The represented playable/meaningful world should include:
- European countries
- colonies and possessions of European countries
- North Africa
- the United States
- Canada
- India
- other overseas territories needed to represent European colonial empires and their wars

Large areas outside that scope may remain **impassable, inert or heavily abstracted terrain** rather than receiving full country/content development.

This is not approval for a fully detailed global 1789 conversion of every independent state.

## A08 — Compatibility baseline: APPROVED

**Decision:** Target the current **HOI4 1.19.x** baseline and **require La Résistance**.

- Other paid DLC should not be required unless separately approved later.
- The descriptor/documentation should state the La Résistance requirement.
- Runtime compatibility still requires an actual game launch on the target version.

## A09 — Alternate-route limits: APPROVED

**Decision:** Add credible historical near-counterfactuals and plausible dynastic/political alternatives, but avoid meme/fantasy routes.

- Alternate paths should have a defensible political, dynastic, diplomatic or ideological basis in the period.
- Implausible novelty paths should not be added merely to increase branch count.

## A10 — Visual and map art direction: APPROVED

**Decision:** Use a **hybrid period presentation**.

- historical/painted portrait and event-scene direction
- engraved/cartographic UI and focus-art direction
- understated period map styling
- avoid excessive modern/gritty-WWII visual language

All replacement assets must remain redistribution-safe and have provenance recorded.

## A11 — Soundtrack direction: APPROVED

**Decision:** Use a mix of:
- original scoring; and
- newly performed/rendered **public-domain Revolutionary/Napoleonic repertoire**

Do not bundle questionable commercial recordings. Record provenance for every shipped track.

## A12 — Translation scope: APPROVED

**Decision:** English only for now.

- English remains the authoritative maintained localisation.
- Community translations may be accepted later.
- Do not create machine-translated release localisation merely to increase language count.

## Next implementation authority

The next development pass is authorized to implement A01–A12 according to the rules above. Any new decision that materially changes these approved principles should be added to this file rather than inferred.
