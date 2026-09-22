#!/usr/bin/env python3
"""Static checks for Roadmap Milestone 2: 1789 diplomacy and bounded wars."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def check(cond, msg):
    if not cond:
        errors.append(msg)

on_actions = (ROOT / "common/on_actions/napoleonic_on_actions.txt").read_text(encoding="utf-8-sig")
setup = (ROOT / "common/scripted_effects/napoleonic_diplomacy_setup.txt").read_text(encoding="utf-8-sig")
events = (ROOT / "events/04_1789_diplomacy.txt").read_text(encoding="utf-8-sig")
states = (ROOT / "common/scripted_effects/napoleonic_state_setup.txt").read_text(encoding="utf-8-sig")

check("napoleonic_setup_1789_map = yes" in on_actions, "startup map setup missing")
check("napoleonic_setup_1789_diplomacy = yes" in on_actions, "startup diplomacy setup missing")
check(on_actions.index("napoleonic_setup_1789_map = yes") < on_actions.index("napoleonic_setup_1789_diplomacy = yes"),
      "diplomacy must initialize after map ownership")

for attacker, defender in (("TUR","RUS"),("SWE","RUS"),("HAB","TUR"),("DEN","SWE")):
    needle = f"declare_war_on = {{ target = {defender} type = annex_everything }}"
    check(needle in setup, f"missing starting war declaration: {attacker} -> {defender}")

for effect in (
    "napoleonic_end_theatre_war",
    "napoleonic_end_russo_swedish_war",
    "napoleonic_end_austro_turkish_war",
    "napoleonic_end_russo_turkish_jassy",
    "napoleonic_end_russo_turkish_ottoman_success",
):
    check(f"{effect} = {{" in setup, f"missing scripted peace effect: {effect}")

check("on_capitulation_immediate" in on_actions, "capitulation guard missing")
for tag in ("RUS","TUR","SWE","HAB","DEN"):
    check(f"tag = {tag}" in on_actions, f"capitulation guard does not reference {tag}")

for treaty_date in ("1789.7.8","1790.8.13","1791.8.3","1792.1.8"):
    check(treaty_date in events, f"missing historical treaty timer around {treaty_date}")

# Jassy must be a bounded transfer. Odessa/Yedisan abstraction is state 192.
jassy = setup.split("napoleonic_end_russo_turkish_jassy = {",1)[1].split("napoleonic_end_russo_turkish_ottoman_success = {",1)[0]
check("transfer_state = 192" in jassy, "Jassy does not transfer the Odessa/Yedisan abstraction")
transfers = [line.strip() for line in jassy.splitlines() if "transfer_state =" in line]
check(transfers == ["transfer_state = 192"], f"Jassy must transfer only state 192, found: {transfers}")

# At the 1789 start Odessa/Yedisan must be Ottoman, not already Russian.
check("state = 192" in states, "state 192 absent from startup map setup")
rus_block = states.split("RUS = { transfer_state = PREV }",1)[0].split("every_state = {")[-1]
check("state = 192" not in rus_block, "state 192 is still assigned to Russia before Jassy")
tur_before = states.split("TUR = { transfer_state = PREV }",1)[0].split("every_state = {")[-1]
check("state = 192" in tur_before, "state 192 is not assigned to the Ottoman Empire in 1789")

# Personal-union and balance-of-power scaffolding.
for needle in (
    "ENG = {\n\t\t\tgive_guarantee = HAN",
    "give_guarantee = POL",
    "give_guarantee = TUS",
    "give_guarantee = NET",
    "give_guarantee = BAV",
    "hre_member_1789",
):
    check(needle in setup, f"missing diplomatic relationship scaffold: {needle}")

if errors:
    print("Diplomacy validation FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("Diplomacy validation passed")
print(" - four opening wars are scripted")
print(" - historical treaty timers are present")
print(" - capitulation guardrails bypass total-war peace conferences")
print(" - Jassy is capped to state 192")
print(" - core 1789 guarantees / dynastic / HRE relationships are present")
