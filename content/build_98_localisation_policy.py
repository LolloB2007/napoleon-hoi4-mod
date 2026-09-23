"""A12 localisation policy: English is the only maintained release language."""
from pathlib import Path

ALLOWED_LANGUAGE = "english"
ALLOWED_HEADER = "l_english:"

def validate_localisation_policy(root, outputs=None):
    errors=[]
    loc=root/'localisation'
    if loc.exists():
        for child in loc.iterdir():
            if child.is_dir() and child.name != ALLOWED_LANGUAGE:
                errors.append(f'unsupported localisation directory: {child.name}')
        english=loc/ALLOWED_LANGUAGE
        if english.exists():
            for path in english.rglob('*.yml'):
                text=path.read_text(encoding='utf-8-sig')
                first=next((line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith('#')),'')
                if first != ALLOWED_HEADER:
                    errors.append(f'bad localisation header: {path.relative_to(root)} -> {first!r}')
    if outputs:
        for path,value in outputs.items():
            if not path.startswith('localisation/'):
                continue
            parts=Path(path).parts
            if len(parts)<3 or parts[1] != ALLOWED_LANGUAGE:
                errors.append(f'generated non-English localisation: {path}')
            text=value.decode('utf-8-sig') if isinstance(value,bytes) else value.removeprefix('\ufeff')
            first=next((line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith('#')),'')
            if first != ALLOWED_HEADER:
                errors.append(f'bad generated localisation header: {path} -> {first!r}')
    if errors:
        raise ValueError('A12 localisation policy violation:\n'+'\n'.join(errors))

def build(root):
    validate_localisation_policy(root)
    return {
      'docs/localisation-policy.md': '''# Localisation policy (A12)

English is the only maintained release localisation.

All checked-in and generated localisation YAML must live under `localisation/english/` and use the `l_english:` header. The content compiler validates generated localisation and the repository tree; tests fail if another maintained language directory is introduced.

Community translations can be reviewed and distributed separately later, but they are not generated automatically and are not part of the maintained release contract. Machine-translated filler is specifically excluded.
'''
    }

def postprocess(outputs,root):
    validate_localisation_policy(root,outputs)
    return {}
