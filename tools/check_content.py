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
    event_namespaces = set()
    for path in (root / 'events').glob('*.txt'):
        tree = load(path)
        for entry in tree:
            if entry.key == 'add_namespace' and isinstance(entry.value, str):
                event_namespaces.add(entry.value)
            if entry.key not in ('country_event', 'news_event', 'state_event'):
                continue
            identifier = entry.scalar('id')
            if identifier in event_ids:
                errors.append(f'duplicate event: {identifier}')
            event_ids.add(identifier)

    # Calls into namespaces owned by this mod must resolve to an event definition.
    # Vanilla/third-party namespaces are deliberately ignored.
    reference_paths = []
    for directory in ('events', 'common'):
        reference_paths.extend((root / directory).rglob('*.txt'))
    for path in reference_paths:
        for entry in walk(load(path)):
            if entry.key not in ('country_event', 'news_event', 'state_event') or not isinstance(entry.value, list):
                continue
            identifier = entry.scalar('id')
            if not identifier or '.' not in identifier:
                continue
            namespace = identifier.split('.', 1)[0]
            if namespace in event_namespaces and identifier not in event_ids:
                errors.append(f'{path.relative_to(root)}: missing event reference {identifier}')

    # Every land OOB pointer/load must resolve to history/units/<name>.txt.
    oob_files = {p.stem for p in (root / 'history' / 'units').glob('*.txt')}
    for directory in ('history/countries', 'events', 'common'):
        for path in (root / directory).rglob('*.txt'):
            for entry in walk(load(path)):
                if entry.key in ('oob', 'set_oob', 'load_oob') and isinstance(entry.value, str):
                    if entry.value not in oob_files:
                        errors.append(f'{path.relative_to(root)}: missing OOB reference {entry.value}')
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
