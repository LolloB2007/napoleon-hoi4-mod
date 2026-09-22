# HOI4 1.19 startup crash fixes

This branch is the startup-safety pass for the Napoleonic Era mod.

## Confirmed startup faults addressed

1. **Broken France focus syntax**
   - The Iberian invasion reward opened an `SPR = {` block whose closing brace was swallowed by a comment.
   - The focus file now parses with balanced braces.

2. **Duplicate state-definition risk**
   - The old build contained hundreds of `history/states/*.txt` overrides generated against older vanilla filenames.
   - HOI4's virtual filesystem replaces by path, not by state ID. If a vanilla filename changes, both the vanilla and mod file can load and define the same state ID.
   - **Do not restore those state override files.**
   - 1789 ownership is now applied through `common/scripted_effects/napoleonic_state_setup.txt` from `on_startup`.

3. **1789 bookmark vs 1936 engine timeline**
   - The mod starts on 5 May 1789, so `NDefines.NGame.START_DATE` is now set to the same timestamp.
   - `END_DATE` is set to 1 January 1821.
   - `replace_path="common/bookmarks"` prevents the vanilla 1936/1939 bookmarks from being mixed into the total-conversion scenario.

4. **Opening event startup hook**
   - `on_startup` now applies the 1789 ownership pass and schedules `napoleonic_timeline.0`.

## Other parse-safety cleanup in the tested build

The local startup-fixed build also stashes references to currently disabled custom technologies and ideas until those systems are restored. Those are gameplay/content errors rather than the primary duplicate-state/focus parser CTDs, but leaving unresolved definitions active makes the error log substantially noisier and can make diagnosis misleading.

## Static validation

The startup-fixed tree was checked with the mod's validators:
- 133 enabled script files scanned
- balanced braces in all scanned files
- 43 unique event IDs, no duplicates
- 91 unique focus IDs, no duplicates
- no enabled `add_ideas`/`remove_ideas` references to the currently stashed idea set

This does not substitute for a real HOI4 executable launch test, so the next validation step after merging is a clean 1.19.x launch with `-debug` and review of `error.log` / `game.log`.
