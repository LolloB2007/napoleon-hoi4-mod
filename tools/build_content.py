#!/usr/bin/env python3
"""Compile sources into checked-in HOI4 files, then apply explicit integration passes."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'content'))
sys.path.insert(0, str(ROOT / 'tools'))
ALLOWED = {'common','events','history','localisation','interface','gfx','docs'}
DOCS = {'README.md','ROADMAP.md','to ask lollo.md','suggestions.md'}


def validate_path(name):
    path = Path(name)
    if not name or path.is_absolute() or '..' in path.parts or not (path.parts[0] in ALLOWED or name in DOCS):
        raise ValueError(f'unsafe generated path: {name}')


def compile_sources(root: Path) -> dict[str, bytes]:
    outputs, modules = {}, []
    for source in sorted((root / 'content').glob('build_*.py')):
        spec = importlib.util.spec_from_file_location(source.stem, source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules.append(module)
        for name, value in module.build(root).items():
            validate_path(name)
            if name in outputs:
                raise ValueError(f'duplicate generated output: {name}')
            outputs[name] = value
    # Named integration passes may deliberately update retained or generated
    # files. These writes still obey the same strict path whitelist.
    for module in modules:
        if hasattr(module, 'postprocess'):
            updates = module.postprocess(dict(outputs), root)
            for name, value in updates.items():
                validate_path(name)
                outputs[name] = value
    encoded = {name: value.encode('utf-8') if isinstance(value,str) else value for name,value in outputs.items()}
    manifest = {name:hashlib.sha256(data).hexdigest() for name,data in sorted(encoded.items())}
    encoded['docs/generated_manifest.json'] = (json.dumps(manifest,indent=2)+'\n').encode()
    return encoded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--root',type=Path,default=ROOT)
    args = parser.parse_args()
    outputs = compile_sources(args.root)
    different = []
    for name,data in outputs.items():
        path = args.root/name
        if not path.is_file() or path.read_bytes()!=data:
            different.append(name)
            if not args.check:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(data)
    print(f'{len(outputs)} generated files; {len(different)} stale before this run.')
    if args.check and different:
        print('\n'.join(different))
        raise SystemExit(1)

if __name__=='__main__': main()
