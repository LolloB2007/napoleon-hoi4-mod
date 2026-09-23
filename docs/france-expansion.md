# French expansion: Milestone 3 implementation slice

29 original focuses are retained. 40 authored policy chapters add 600 focuses, and one cross-route administrative capstone brings the tree to **630**. There are **120 new policy events** and 80 chapter-related spirits (40 temporary programmes, 40 persistent settlements).

The new chapter durations in days are: {14: 120, 21: 200, 28: 120, 35: 120, 49: 27, 70: 13}. A focus is not a promise that every route can take it: each chapter contains exclusive policies, and Girondin/Jacobin programmes are mutually exclusive. The original four political routes remain the main paths.

Each chapter has two exclusive forks, parallel preparation work, three event dilemmas and a concluding institution. Events distinguish a funded policy from a lower-cost settlement. Resource checks are repeated on execution. Rewards and event choices have completion flags to prevent repeated payouts. No chapter grants unrestricted territorial cores, seizes a foreign state or invents a new political route.

The new focuses are grouped in four columns of chapter panels below the retained tree. Coordinates are statically unique; actual rendering, line routing and usability at this scale must be checked inside HOI4.

The existing French event files are retained under content/legacy and normalized through a parser for route/duplicate guards. Under A01, historical dates are minimum gates on the relevant legacy focuses; event progression is route/state-driven. The Directory follows the Thermidor transition so a republic that restrains the Terror is not stranded before the Consulate. Current rulers are not accidentally retired by an event ostensibly about a deposed king. Collective governments and restoration leaders receive explicit legacy leader creation where necessary.

This is not a declaration that all of Milestone 3 is finished. Deep scripted campaigns, state-level Vendee warfare, a complete modern-character conversion, active client-state management, final coring policy, full blockade enforcement and engine-tested balance remain further work. A01 chronology is implemented here; outcome-aware bounded peace is implemented by the stacked A03 pass.

The focus index JSON records IDs, titles, routes, durations, coordinates, prerequisites and exclusions. Names and event subjects are authored in france_catalogue.py; engine repetition is generated, not hand-copied.
