# To ask Lollo

**Current branch: French decision-driven campaign mechanics implemented in source; full HOI4 runtime validation pending**

This is the owner-decision register. A01-A12 are approved; implementation status is tracked separately. Existing French routes, ordinary implementation and validation are authorized. The current owner target is 600-650 French focuses, 350-400 for each other major, and 150-200 for each secondary campaign with at least 30-40 country-specific focuses. Approving a PR does not approve all proposals listed here.

## A01: Calendar model

**Approved.** APPROVED: historical dates are minimum-date focus gates only; events, wars and peace deals are state-driven.

## A02: Campaign end

**Approved.** APPROVED: remove the practical campaign end and allow open-ended continuation.

## A03: Alternate peace outcomes

**Approved.** APPROVED: settlements follow the actual victor and war objectives; no unrestricted annexation.

## A04: Coring policy

**Approved.** APPROVED: no broad conquest coring; only historical/formable cores, with targeted compliance support where appropriate.

## A05: Formable catalogue

**Approved.** APPROVED IN PRINCIPLE: conventional and limited credible alternate formables with explicit founders and borders.

## A06: Clients and releasables

**Approved.** APPROVED: standard HOI4 puppet relationships are the default; never transfer unrelated third-party land.

## A07: Geographic scope

**Approved.** APPROVED: Europe plus relevant colonial possessions, North Africa, USA, Canada and India; irrelevant regions may remain inert/abstract.

## A08: Compatibility baseline

**Approved.** APPROVED: target HOI4 1.19.x and require La Résistance; runtime compatibility still needs a real launch.

## A09: Alternate-route limits

**Approved.** APPROVED: credible historical near-counterfactuals and plausible dynastic/political alternatives; no meme/fantasy routes.

## A10: Visual and map art direction

**Approved.** APPROVED: painted/historical scenes and portraits, engraved/cartographic UI and focus art, understated period map styling.

## A11: Soundtrack direction

**Approved.** APPROVED: original scoring plus newly rendered public-domain Revolutionary/Napoleonic repertoire, with provenance.

## A12: Translation scope

**Approved.** APPROVED: English only for now; community translations may be accepted later, but no machine-translated release padding.

## Not approval blockers

Namespacing, missing references, scope corrections, finite costs, cooldowns, idempotency, localisation encoding, tests and preserving existing work can proceed. Prototype balance numbers remain provisional until campaign testing.

## Territorial registry status

The registry below is implementation data under approved A04/A05 policy. Approved entries require explicit borders and attribution in source.

| ID | Proposal | State IDs | Status |
|---|---|---|---|
| savoy | Savoy | [735] | Approved (A04) |
| austrian_netherlands | Austrian Netherlands (draft map abstraction) | [6] | Approved (A04) |
| italian_kingdom | Kingdom of Italy | [2, 114, 115, 117, 156, 157, 158, 160, 161, 162, 163, 735, 736, 849, 852] | Approved (A05) |
| german_confederation | German Confederation | [50, 52, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67, 763, 978] | Approved (A05) |
| scandinavian_union | Scandinavian Union | [37, 38, 58, 99, 101, 110, 111, 124, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 337, 666, 722, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 926, 927] | Approved (A05) |
| restored_commonwealth | Restored Commonwealth | [10, 11, 85, 86, 87, 88, 89, 92, 93, 188, 189, 198, 199, 200, 201, 202, 204, 205, 206, 814, 815] | Approved (A05) |
| danubian_federation | Danubian Federation | [4, 6, 9, 39, 43, 69, 70, 71, 73, 74, 75, 76, 80, 82, 83, 84, 90, 91, 102, 103, 109, 152, 153, 154, 155, 159, 664, 848, 850, 853, 972, 973, 974, 975, 976, 977] | Approved (A05/A09) |
| rhine_federation | Rhine Federation | [50, 52, 53, 54, 55, 60, 65, 978] | Approved (A05/A06) |
