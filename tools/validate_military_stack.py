#!/usr/bin/env python3
"""Static consistency checks for the restored Napoleonic military stack.

This does not replace an in-game HOI4 launch test. It catches the cross-file
mistakes that otherwise turn into opaque parser/database errors: missing techs,
missing subunits/equipment, missing technology categories, unresolved OOB
battalions, and accidental reintroduction of known vanilla equipment IDs.
"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def texts(glob):
    return [(p, p.read_text(encoding='utf-8-sig')) for p in ROOT.glob(glob) if '.disabled' not in p.parts]

tech_files = texts('common/technologies/*.txt')
unit_files = texts('common/units/napoleonic_*.txt')
equip_files = texts('common/units/equipment/*.txt')
tag_files = texts('common/technology_tags/*.txt')
oob_files = texts('history/units/*.txt')
country_files = texts('history/countries/*.txt')

# Top-level-ish identifiers are distinctive enough in these dedicated files.
tech_ids = set()
for _, s in tech_files:
    tech_ids |= set(re.findall(r'^\s*([A-Za-z0-9_]+)\s*=\s*\{\s*$', s, re.M))
# Remove structural/nested keys that may be caught by the loose pattern.
tech_ids -= {'technologies','path','folder','ai_will_do','modifier','OR','AND','NOT','categories','xor'}

unit_ids = set()
for _, s in unit_files:
    m = re.search(r'sub_units\s*=\s*\{', s)
    if not m: continue
    # Custom sub-unit IDs always begin one tab in these files.
    unit_ids |= set(re.findall(r'^\t([a-z][a-z0-9_]+)\s*=\s*\{', s, re.M))

equip_ids = set()
for _, s in equip_files:
    m = re.search(r'equipments\s*=\s*\{', s)
    if not m: continue
    equip_ids |= set(re.findall(r'^\t([A-Za-z0-9_]+)\s*=\s*\{', s, re.M))

categories = set()
for _, s in tag_files:
    block = re.search(r'technology_categories\s*=\s*\{(.*?)\n\}', s, re.S)
    if block:
        categories |= set(re.findall(r'^\s*([A-Za-z0-9_]+)\s*$', block.group(1), re.M))
# Vanilla category used intentionally by doctrines.
categories.add('land_doctrine')

errors=[]; warnings=[]

def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

# Starting country technology references.
for p,s in country_files:
    for block in re.findall(r'set_technology\s*=\s*\{(.*?)\n\}', s, re.S):
        for tid in re.findall(r'^\s*([A-Za-z0-9_]+)\s*=\s*[01]\b', block, re.M):
            if tid not in tech_ids:
                err(f'{p.relative_to(ROOT)}: starting technology not defined: {tid}')

# Tech -> equipment/subunit/category references.
for p,s in tech_files:
    for block in re.findall(r'enable_equipments\s*=\s*\{([^}]*)\}', s, re.S):
        for eid in re.findall(r'\b[A-Za-z0-9_]+\b', block):
            if eid not in equip_ids:
                err(f'{p.relative_to(ROOT)}: enable_equipments target not defined: {eid}')
    for block in re.findall(r'enable_subunits\s*=\s*\{([^}]*)\}', s, re.S):
        for uid in re.findall(r'\b[A-Za-z0-9_]+\b', block):
            if uid not in unit_ids:
                err(f'{p.relative_to(ROOT)}: enable_subunits target not defined: {uid}')
    for block in re.findall(r'categories\s*=\s*\{([^}]*)\}', s, re.S):
        for cat in re.findall(r'\b[A-Za-z0-9_]+\b', block):
            if cat not in categories:
                # Vanilla categories outside our declaration are legitimate, but tech
                # files currently should only use land_doctrine + our custom tags.
                err(f'{p.relative_to(ROOT)}: technology category not declared: {cat}')

# Subunit equipment needs.
for p,s in unit_files:
    for block in re.findall(r'need\s*=\s*\{([^}]*)\}', s, re.S):
        for eid in re.findall(r'\b([A-Za-z0-9_]+)\s*=\s*[-0-9.]+', block):
            if eid not in equip_ids:
                err(f'{p.relative_to(ROOT)}: subunit equipment archetype not defined: {eid}')

# OOB battalion/support IDs.
for p,s in oob_files:
    for uid in re.findall(r'^\s*([a-z][a-z0-9_]+)\s*=\s*\{\s*x\s*=\s*\d+\s+y\s*=\s*\d+\s*\}', s, re.M):
        if uid not in unit_ids:
            err(f'{p.relative_to(ROOT)}: OOB subunit not defined: {uid}')

# Explicit starting OOBs should exist for the five majors.
for tag in ('FRA','ENG','HAB','PRU','RUS'):
    expected = ROOT / 'history' / 'units' / f'{tag}_1789.txt'
    if not expected.exists(): err(f'missing standing OOB file: history/units/{tag}_1789.txt')
    cf = next((p for p,_ in country_files if p.name.startswith(tag+' ')), None)
    if not cf or f'oob = "{tag}_1789"' not in cf.read_text(encoding='utf-8-sig'):
        err(f'{tag}: country history does not load {tag}_1789')

# Idea equipment_bonus targets must resolve to an enabled equipment ID.
for p,s in texts('common/ideas/*.txt'):
    for block in re.findall(r'equipment_bonus\s*=\s*\{(.*?)\n\s*\}', s, re.S):
        for eid in re.findall(r'^\s*([A-Za-z0-9_]+)\s*=\s*\{', block, re.M):
            if eid not in equip_ids:
                err(f'{p.relative_to(ROOT)}: equipment_bonus target not defined: {eid}')

# Known vanilla equipment IDs must not be redefined from a second path.
known_vanilla = {
    'artillery_equipment','artillery_equipment_1','artillery_equipment_2','artillery_equipment_3',
    'support_equipment','support_equipment_1'
}
for eid in sorted(equip_ids & known_vanilla):
    err(f'custom equipment redefines known vanilla equipment ID: {eid}')

# We deliberately use vanilla-safe classifications on custom land subunits.
for p,s in unit_files:
    if p.name == 'napoleonic_artillery.txt' and 'category_artillery' not in s:
        err('artillery subunits are missing category_artillery')
    if p.name == 'napoleonic_support.txt' and 'category_support_battalions' not in s:
        err('support subunits are missing category_support_battalions')
    if p.name == 'napoleonic_infantry.txt' and 'category_all_infantry' not in s:
        err('infantry subunits are missing category_all_infantry')
    if p.name == 'napoleonic_cavalry.txt' and 'cavalry = yes' not in s:
        err('cavalry subunits are missing cavalry = yes classification')

# Legacy category assignment form caused 1.18 errors and must never return.
for p,s in tech_files:
    if re.search(r'^\s*category_[A-Za-z0-9_]+\s*=\s*1\s*$', s, re.M):
        err(f'{p.relative_to(ROOT)}: legacy category_X = 1 technology syntax found')

print(f'Technologies: {len(tech_ids)}')
print(f'Custom subunits: {len(unit_ids)}')
print(f'Custom equipment IDs: {len(equip_ids)}')
print(f'Custom technology categories: {len(categories)-1}')
if warnings:
    print('\nWarnings:')
    for x in warnings: print(' -', x)
if errors:
    print('\nERRORS:')
    for x in errors: print(' -', x)
    sys.exit(1)
print('\nMilitary stack cross-references resolve.')
