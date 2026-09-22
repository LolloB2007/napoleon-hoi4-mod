# Reusable era mechanics (Milestone 6 slice)

Eight bounded meters: treasury, debt, legitimacy, fervor, war exhaustion, national army prestige, administrative/military reform and foreign-campaign supply pressure. They are explicitly game abstractions.

Initialization is idempotent. The monthly hook runs once per eligible country, without a nested world scan. Occupation checks only run during war. Peace restores capacity and reduces exhaustion; high debt drains fiscal capacity; long foreign campaigns increase pressure.

Twelve decisions have finite political-power costs, resource checks and 90-365 day cooldowns. Resource predicates are repeated at effect execution. Levee is restricted to revolutionary France at war. No decision deletes units, creates territorial cores or changes faction membership.

Eleven national spirits represent threshold effects and two temporary paid policies. Severe and ordinary exhaustion are mutually exclusive. Values clamp to 0-100 after pulses and decisions. Battle hooks affect national army prestige, not individual-general prestige.

This is not all of Milestone 6: individual leader reputation, nationalism, state-specific occupation politics, client management and a fuller economic model remain separate work. Unit tests exercise the reference resource model and generated syntax; they are not HOI4 runtime tests. Balance numbers are provisional.
