#!/usr/bin/env python3
"""Structural validation. Passing does not prove HOI4 runtime compatibility."""
from pathlib import Path
import argparse
import re
import sys
from pdx import load, walk, focus_graph, validate_graph


def validate(root: Path) -> list[str]:
    errors = []
    for directory in ('common', 'history', 'events', 'interface'):
        for path in sorted((root / directory).rglob('*')):
            if path.suffix not in ('.txt', '.gui', '.gfx'):
                continue
            try:
                load(path)
            except (ValueError, UnicodeError) as exc:
                errors.append(f'{path.relative_to(root)}: {exc}')
    try:
        graph = focus_graph(root)
        validate_graph(graph)
        for path in (root / 'common/national_focus').glob('*.txt'):
            for entry in walk(load(path)):
                if entry.key == 'shared_focus' and isinstance(entry.value, str) and entry.value not in graph:
                    errors.append(f'{path.name}: missing shared-focus root {entry.value}')
    except ValueError as exc:
        errors.append(str(exc))
    for path in (root / 'common/country_tags').glob('*.txt'):
        for entry in load(path):
            if isinstance(entry.value, str) and not (root / 'common' / entry.value).is_file():
                errors.append(f'{entry.key}: missing common/{entry.value}')
    event_ids = set()
    for path in (root / 'events').glob('*.txt'):
        for entry in load(path):
            if entry.key not in ('country_event', 'news_event', 'state_event'):
                continue
            identifier = entry.scalar('id')
            if identifier in event_ids:
                errors.append(f'duplicate event: {identifier}')
            event_ids.add(identifier)
    for path in (root / 'localisation').rglob('*.yml'):
        raw = path.read_bytes()
        if not raw.startswith(b'\xef\xbb\xbf'):
            errors.append(f'{path.relative_to(root)}: missing UTF-8 BOM')
    for path in (root / 'common/scripted_effects').glob('*.txt'):
        for entry in walk(load(path)):
            if entry.key in ('add_state_core', 'remove_state_core'):
                errors.append(f'{path.name}: use state scope add_core_of/remove_core_of, not {entry.key}')
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    issues = validate(args.root)
    for issue in issues:
        print('ERROR:', issue)
    print(f'Structural validation: {len(issues)} error(s). No engine launch performed.')
    sys.exit(bool(issues))
