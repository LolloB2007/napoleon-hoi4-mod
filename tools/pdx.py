"""Small structural parser for Clausewitz scripts, not an engine emulator."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import json

TOKEN = re.compile(r'\s+|#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|[<>!?]?=|[<>]|[^\s{}=<>!?"#]+')

@dataclass
class Entry:
    key: str
    value: str | list[Entry]
    op: str = '='

    def children(self, key: str) -> list[Entry]:
        return [e for e in self.value if e.key == key] if isinstance(self.value, list) else []

    def scalar(self, key: str, default: str = '') -> str:
        matches = self.children(key)
        return str(matches[0].value) if matches else default


def atom(token: str) -> str:
    if not token.startswith('"'):
        return token
    escapes = {'n': '\n', 't': '\t', 'r': '\r', '"': '"', '\\': '\\'}
    return re.sub(r'\\(.)', lambda m: escapes.get(m[1], '\\' + m[1]), token[1:-1])


def dumps(entries: list[Entry], depth: int = 0) -> str:
    def encode(value):
        if value and re.fullmatch(r'[A-Za-z0-9_@.:-]+', value):
            return value
        return json.dumps(value, ensure_ascii=False)
    lines = []
    for entry in entries:
        prefix = '\t' * depth + encode(entry.key)
        if not entry.op:
            lines.append(prefix)
        elif isinstance(entry.value, list):
            lines.append(prefix + ' ' + entry.op + ' {')
            lines.append(dumps(entry.value, depth + 1).rstrip('\n'))
            lines.append('\t' * depth + '}')
        else:
            lines.append(prefix + ' ' + entry.op + ' ' + encode(entry.value))
    return '\n'.join(lines) + '\n'


def parse(text: str) -> list[Entry]:
    text = text.lstrip('\ufeff')
    tokens: list[str] = []
    end = 0
    for match in TOKEN.finditer(text):
        if match.start() != end:
            raise ValueError(f'unrecognized token near offset {end}: {text[end:end+30]!r}')
        end = match.end()
        token = match.group()
        if not token.isspace() and not token.startswith('#'):
            tokens.append(token)
    if end != len(text):
        raise ValueError(f'unrecognized trailing token at {end}')
    pos = 0
    def block(nested: bool = False) -> list[Entry]:
        nonlocal pos
        result: list[Entry] = []
        while pos < len(tokens):
            key = tokens[pos]
            pos += 1
            if key == '}':
                if not nested:
                    raise ValueError('unexpected closing brace')
                return result
            if key in ('{', '=', '>', '<', '>=', '<=', '!=', '?='):
                raise ValueError(f'unexpected token {key!r}')
            key = atom(key)
            if pos == len(tokens) or tokens[pos] not in ('=', '>', '<', '>=', '<=', '!=', '?='):
                result.append(Entry(key, '', ''))
                continue
            op = tokens[pos]
            pos += 1
            if pos >= len(tokens) or tokens[pos] == '}':
                raise ValueError(f'missing value for {key}')
            value = tokens[pos]
            pos += 1
            result.append(Entry(key, block(True) if value == '{' else atom(value), op))
        if nested:
            raise ValueError('unclosed block')
        return result
    return block()


def load(path: Path) -> list[Entry]:
    return parse(path.read_text(encoding='utf-8-sig'))


def walk(entries: list[Entry]):
    for entry in entries:
        yield entry
        if isinstance(entry.value, list):
            yield from walk(entry.value)


def focus_graph(root: Path) -> dict[str, Entry]:
    result: dict[str, Entry] = {}
    for path in sorted((root / 'common/national_focus').glob('*.txt')):
        for entry in walk(load(path)):
            if entry.key not in ('focus', 'shared_focus', 'joint_focus') or not isinstance(entry.value, list):
                continue
            identifier = entry.scalar('id')
            if not identifier:
                raise ValueError(f'{path}: focus has no id')
            if identifier in result:
                raise ValueError(f'duplicate focus: {identifier}')
            result[identifier] = entry
    return result


def validate_graph(graph: dict[str, Entry]) -> None:
    edges = {}
    for identifier, entry in graph.items():
        targets = [f.value for p in entry.children('prerequisite') for f in p.children('focus')]
        exclusive = [f.value for p in entry.children('mutually_exclusive') for f in p.children('focus')]
        for target in targets + exclusive:
            if target not in graph:
                raise ValueError(f'{identifier}: missing focus reference {target}')
        edges[identifier] = targets
    done, visiting = set(), set()
    def visit(identifier):
        if identifier in visiting:
            raise ValueError(f'focus prerequisite cycle at {identifier}')
        if identifier in done:
            return
        visiting.add(identifier)
        for target in edges[identifier]:
            visit(target)
        visiting.remove(identifier)
        done.add(identifier)
    for identifier in edges:
        visit(identifier)
